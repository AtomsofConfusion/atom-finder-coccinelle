from collections import defaultdict
import csv
import difflib
import json
from pathlib import Path
import re
import tempfile
from typing import Dict, List, Set, Tuple

import pygit2

from src import ROOT_DIR
from src.analysis.parsing import run_coccinelle_for_file_at_commit
from src.analysis.git import get_diff
from src.analysis.utils import append_to_json
from src.run_cocci import CocciPatch
from src.log import logger


atom_name_to_patch_mapping = {
    "assignment-as-value": CocciPatch.ASSIGNMENT_AS_VALUE,
    "conditional": CocciPatch.CONDITIONAL_OPERATOR,
    "implicit-predicate": CocciPatch.IMPLICIT_PREDICATE,
    "repurposed_variable": CocciPatch.REPURPOSED_VARIABLE,
    "pre-increment": CocciPatch.PRE_INCDEC,
    "post-increment": CocciPatch.POST_INCDEC,
    "type_conversion": CocciPatch.TYPE_CONVERSION,
    "logic-as-controlflow": CocciPatch.LOGIC_AS_CONTROLFLOW,
    "literal-encoding": CocciPatch.CHANGE_OF_LITERAL_ENCODING,
    "comma-operator": CocciPatch.COMMA_OPERATOR,
    "operator-precedence": CocciPatch.OPERATOR_PRECEDENCE,
}

atom_path_to_name_mapping = {
    patch: name for name, patch in atom_name_to_patch_mapping.items()
}


def group_consecutive_lines(line_map):
    grouped_lines = {}
    for (file, line), match in line_map.items():
        if file not in grouped_lines:
            grouped_lines[file] = []

        current_group = grouped_lines[file]
        if (
            not current_group
            or current_group[-1][-1][0].old_lineno != line.old_lineno - 1
        ):
            current_group.append([])  # Start a new group

        current_group[-1].append((line, match))

    return grouped_lines


def group_added_and_removed_lines(
    added_removed_lines_map: Dict[
        Tuple[str, pygit2.DiffLine], Tuple[pygit2.DiffLine, float]
    ],
    current_commit_data: List[Dict[str, any]],
    atom_types_to_find: Set[str] = None,
) -> Tuple[
    Dict[str, List[pygit2.DiffLine]],
    Dict[pygit2.DiffLine, List[Dict[str, any]]],
    Set[str],
]:
    """
    This function processes a mapping of file diffs to identify relevant atom changes,
    groups them by file, and applies filters based on specified atom types.

    Args:
        added_removed_lines_map: A dictionary mapping a tuple of (file name, removed DiffLine)
            to a tuple of (added DiffLine, similarity index).
        current_commit_data: A list of dictionaries containing atom data for the current commit.
        atom_types_to_find: A set of atom types to filter the atoms by; if None, all atom types are processed.

    Returns:
        A tuple containing:
        - A dictionary mapping file names to lists of added DiffLines.
        - A dictionary mapping removed DiffLines to lists of associated atom data.
        - A set of atom patches that were identified and need processing.
    """
    processed_pairs = defaultdict(list)
    patches = set()
    added_files_map = defaultdict(list)
    removed_atoms = defaultdict(list)
    for file_removed_diff, added in added_removed_lines_map.items():
        added_diff, similarity_index = added
        if similarity_index == 1:
            # lines are identical, there is no point in analyzing
            continue
        file, removed_diff = file_removed_diff
        removed_content = removed_diff.content.strip()
        added_content = added_diff.content.strip()
        if added_content in processed_pairs.get(removed_content, []):
            continue
        processed_pairs[removed_content].append(added_content)

        for atom_data in current_commit_data:
            if (
                atom_data["file"] == file
                and atom_data["start_row"] == removed_diff.old_lineno
            ):
                atom_name = atom_data["atom_name"]
                patch = atom_name_to_patch_mapping[atom_name]
                if not atom_types_to_find or patch in atom_types_to_find:
                    patches.add(patch)
                removed_atoms[removed_diff].append(atom_data)

        added_files_map[file].append(added[0])

    return added_files_map, removed_atoms, patches


def load_last_processed(last_processed_file):
    """Load the last processed commit from a file."""
    if last_processed_file.is_file():
        try:
            last_processed = json.loads(last_processed_file.read_text())
            return last_processed.get("commit")
        except json.JSONDecodeError:
            return None
    return None


def save_last_processed(last_processed_file, last_commit):
    """Save the last processed commit to a file."""
    last_processed_file.write_text(json.dumps({"commit": last_commit}, indent=4))


def map_similar_lines(removed, added):

    def _calculate_combined_score(r_line, a_line, max_line_distance):
        similarity = difflib.SequenceMatcher(
            None, r_line.content.strip(), a_line.content.strip()
        ).ratio()
        # Calculate proximity as a normalized value
        distance = abs(r_line.old_lineno - a_line.new_lineno)
        proximity = 1 - (distance / max_line_distance)
        proximity = max(0, proximity)  # Ensure the proximity is not negative

        # Combine these scores, you can adjust weights here
        combined_score = 0.7 * similarity + 0.3 * proximity
        return combined_score

    similarity_threshold = 0.8
    all_potential_matches = []

    # Collect all potential matches that exceed the threshold
    for r_file, r_lines in removed.items():
        for r_line in r_lines:

            r_line_content = r_line.content.strip()
            if r_line_content in ("{", "}") or "else" in r_line_content:
                continue
            if r_file in added:
                for a_line in added[r_file]:
                    score = _calculate_combined_score(r_line, a_line, 100)
                    if score > similarity_threshold:
                        all_potential_matches.append((score, r_file, r_line, a_line))

    # Sort all potential matches by descending similarity ratio
    all_potential_matches.sort(reverse=True, key=lambda x: x[0])

    best_matches = {}
    assigned_added = {}

    for score, r_file, r_line, a_line in all_potential_matches:
        current_best = assigned_added.get(
            r_line.old_lineno, (None, 0)
        )  # Get current best match and its score
        if score > current_best[1]:
            if current_best[0] is not None:
                # Previous match is superseded, remove the previous best match
                del best_matches[(r_file, current_best[0])]
            # Assign the new best match
            best_matches[(r_file, r_line)] = (a_line, score)
            assigned_added[r_line.old_lineno] = (a_line, score)
        elif r_line.old_lineno not in assigned_added:
            # If the added line is not yet used, assign it
            best_matches[(r_file, r_line)] = (a_line, score)
            assigned_added[r_line.old_lineno] = (a_line, score)

    return best_matches


def find_atoms_added_lines(temp_dir, added_lines, commit, patches_to_run):
    loaded_headers = defaultdict(list)
    invalid_headers = defaultdict(list)

    # skip all patches that are not contained by pathes to run
    patches_to_skip = [
        cocci_patch for cocci_patch in CocciPatch if cocci_patch not in patches_to_run
    ]

    all_atoms = []

    for file_name, added in added_lines.items():
        added_line_numbers = [line.new_lineno for line in added]

        atoms = run_coccinelle_for_file_at_commit(
            repo,
            file_name,
            commit,
            added_line_numbers,
            temp_dir,
            loaded_headers,
            invalid_headers,
            patches_to_skip,
        )
        for atom in atoms:
            all_atoms.append(
                {
                    "atom_name": atom[0],
                    "file": atom[1],
                    "start_row": int(atom[2]),
                    "start_col": int(atom[3]),
                    "code": atom[6],
                }
            )

    return all_atoms


def find_removed_atoms(
    repo,
    atoms_data,
    output_file,
    last_processed_file,
    atom_types_to_find=None,
    restart=False,
):

    last_processed_commit = None
    last_processed = {}

    last_processed_commit = None
    if not restart:
        last_processed_commit = load_last_processed(last_processed_file)

    found_first = None
    for commit_sha, commit_data in atoms_data.items():
        if last_processed_commit and not found_first:
            if commit_sha == last_processed_commit:
                found_first = True
            continue

        logger.info(f"Current commit {commit_sha}")
        atoms_diff = []

        removed_lines_in_files = {
            (data["file"], data["start_row"]) for data in commit_data
        }
        # find all atoms linked with the same file and then analyze added lines

        commit = repo[commit_sha]
        added_lines, removed_lines = get_diff(repo, commit)

        removed_lines_with_atoms = defaultdict(list)
        for line_data in removed_lines_in_files:
            file, line_no = line_data
            for diff_line in removed_lines[file]:
                if diff_line.old_lineno == line_no:
                    removed_lines_with_atoms[file].append(diff_line)
                    break

        # map removed lines to added lines in order to skip atoms that were removed and added
        # that is, not modified in that diff
        lines_map = map_similar_lines(removed_lines_with_atoms, added_lines)
        if lines_map:
            added_files_map, removed_atoms, patches = group_added_and_removed_lines(
                lines_map, commit_data, atom_types_to_find
            )

            if len(patches):
                with tempfile.TemporaryDirectory() as temp_dir:
                    added_atoms = find_atoms_added_lines(
                        temp_dir, added_files_map, commit, patches
                    )
                    for file_removed_diff, added in lines_map.items():
                        added_diff = added[0]
                        file, removed_diff = file_removed_diff
                        current_atoms_diff = []

                        if removed_diff in removed_atoms:
                            removed_atoms_data = removed_atoms[removed_diff]
                            for removed_atom in removed_atoms_data:
                                if (
                                    atom_types_to_find
                                    and atom_name_to_patch_mapping[
                                        removed_atom["atom_name"]
                                    ]
                                    not in atom_types_to_find
                                ):
                                    continue

                                atom_name = removed_atom["atom_name"]
                                removed_and_added = any(
                                    added_data["atom_name"] == atom_name
                                    and added_data["start_row"] == added_diff.new_lineno
                                    for added_data in added_atoms
                                )

                                if not removed_and_added and update_of_interest(
                                    removed_diff, added_diff, atom_name
                                ):
                                    current_atoms_diff.append(
                                        {
                                            "atom_name": atom_name,
                                            "file": removed_atom["file"],
                                            "commit": removed_atom["commit"],
                                            "start_row": removed_atom["start_row"],
                                            "start_col": removed_atom["start_col"],
                                            "added_row": added_diff.new_lineno,
                                            "removed_code": removed_diff.content,
                                            "added_code": added_diff.content,
                                        }
                                    )

                        # Filter and extend the atoms differences list
                        filtered_atoms = filter_atoms(current_atoms_diff)
                        atoms_diff.extend(filtered_atoms)

        atoms_json = [
            {
                "atom": data[0],
                "file": data[1],
                "commit": data[2],
                "start-row": data[3],
                "added-row": data[5],
                "removed": data[7],
                "added": data[8],
                "commit-message": commit.message,
            }
            for data in atoms_diff
            if atom_types_to_find is None
            or atom_name_to_patch_mapping[data[0]] in atom_types_to_find
        ]

        if atoms_json:
            append_to_json(output_file, atoms_json)
        last_processed["commit"] = commit_sha
        last_processed_file.write_text(json.dumps(last_processed, indent=4))


def filter_atoms(data):
    # Group the data by 'start_row'
    grouped_by_row = {}
    for item in data:
        start_row = item[3]  # 'start_row' is the fourth element
        if start_row not in grouped_by_row:
            grouped_by_row[start_row] = []
        grouped_by_row[start_row].append(item)

    # Function to determine the "largest" code (assuming largest by string length)
    def get_largest_code(items):
        return max(items, key=lambda x: len(x[6]))  # 'code' is the seventh element

    # Filter out only the largest codes for each start_row
    filtered_data = []
    for items in grouped_by_row.values():
        if len(items) > 1:
            largest_item = get_largest_code(items)
            filtered_data.append(largest_item)
        else:
            filtered_data.extend(items)

    if len(data) > len(filtered_data):
        print("something removed here...")
    return filtered_data


def contains_ternary_operator(expression):
    # This regex looks for patterns resembling ternary operations.
    pattern = re.compile(r"\?.*:")
    return bool(pattern.search(expression))


def check_if_parentheses_added(removed_diff, added_diff):
    # I'd like to parse this and use clang to compare the lines
    # however, there are occasional parsing issues (probably something missing)

    def count_operators_and_parentheses(code):
        # Remove strings (both single and double quoted)
        code_without_strings = re.sub(r'".*?"|\'.*?\'', "", code)

        # Remove single-line and multi-line comments
        code_clean = re.sub(
            r"//.*?$|/\*.*?\*/",
            "",
            code_without_strings,
            flags=re.DOTALL | re.MULTILINE,
        )

        # Define regex patterns for unary and binary operators
        unary_operators = [
            r"\b\+\+",
            r"\b--",  # Increment and decrement
            r"(?<!\w)!(?=\s*\()",  # Logical NOT directly followed by an opening parenthesis with optional whitespace
            r"(?<!\w)!(?=\s*\w)",  # Logical NOT directly followed by a word character with optional whitespace
            r"(?<=\()\s*-\s*(?=\d|\w)",  # Negative numbers or negation directly after an opening parenthesis
        ]
        binary_operators = [
            r"(?<!\+)\+(?!\+)",
            r"(?<!-)-(?!-)",
            r"\*",
            r"/",
            r"%",
            r"==",
            r"!=",
            r"<=",
            r">=",
            r"&&",
            r"\|\|",
            r"&(?!\&)",
            r"\|(?!\|)",
            r"\^",
            r"<<",
            r">>",
            r"(?<!<)<(?!<)",
            r"(?<!>)>(?!>)",
        ]
        parentheses = [r"\(", r"\)"]

        # Count occurrences
        counts = {
            "unary": sum(
                len(re.findall(pattern, code_clean)) for pattern in unary_operators
            ),
            "binary": sum(
                len(re.findall(pattern, code_clean)) for pattern in binary_operators
            ),
            "parentheses": sum(
                len(re.findall(pattern, code_clean)) for pattern in parentheses
            ),
        }

        return counts

    removed_counts = count_operators_and_parentheses(removed_diff.content)
    added_counts = count_operators_and_parentheses(added_diff.content)
    # this isn't very robust at all
    # need to parse, but figure out parsing issues first
    return (
        removed_counts["unary"] == added_counts["unary"]
        and removed_counts["binary"] == added_counts["binary"]
        and removed_counts["parentheses"] < added_counts["parentheses"]
    )


def update_of_interest(removed_diff, added_diff, atom):
    if atom == "operator-precedence":
        result = check_if_parentheses_added(removed_diff, added_diff)
        return result
    return True


def read_and_sort_data(filename):

    atoms_by_commit = defaultdict(list)

    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            if len(row) != 6:
                raise ValueError("Row does not contain the correct number of fields")

            data = {
                "atom_name": row[0],
                "file": row[1],
                "commit": row[2],
                "start_row": int(row[3]),
                "start_col": int(row[4]),
                "code": row[5],
            }

            atoms_by_commit[data["commit"]].append(data)

    return atoms_by_commit


if __name__ == "__main__":
    filename = "atoms2.csv"
    repo_path = (
        ROOT_DIR.parent / "atoms/projects/linux"
    )  # Change this to your repo path
    output = Path("results/removed/atoms.json")
    last_processed_file = Path("last_processed/removed/last_processed.json")
    output.parent.mkdir(exist_ok=True)
    last_processed_file.parent.mkdir(exist_ok=True)
    repo = pygit2.Repository(repo_path)
    atoms_data = read_and_sort_data(filename)
    find_removed_atoms(
        repo, atoms_data, output, last_processed_file, [CocciPatch.CONDITIONAL_OPERATOR]
    )
