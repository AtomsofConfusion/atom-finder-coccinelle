from collections import defaultdict
import csv
import difflib
import json
from pathlib import Path
import tempfile

import pygit2

from src import ROOT_DIR
from src.analysis.cocci_analysis import run_coccinelle_for_file_at_commit
from src.analysis.git import get_diff
from src.analysis.utils import append_rows_to_csv
from src.run_cocci import CocciPatch


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


def map_similar_lines(removed, added):
    similarity_threshold = 0.8
    mappings = {}

    for r_file, r_lines in removed.items():
        for r_line in r_lines:
            r_line_content = r_line.content.strip()
            if r_line_content in ("{", "}") or "else" in r_line_content:
                continue
            best_match = None
            best_ratio = 0
            for _, a_lines in added.items():
                for a_line in a_lines:
                    a_line_content = a_line.content.strip()
                    ratio = difflib.SequenceMatcher(None, r_line_content, a_line_content).ratio()
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_match = (a_line, best_ratio)
            
            if best_ratio > similarity_threshold:
                mappings[(r_file, r_line)] = best_match

            # if best_match:
            #     added[r_file].remove(best_match[0]) 
    
    return mappings


def find_atoms_added_lines(added_lines, commit, patches_to_run):
    loaded_headers = defaultdict(list)
    invalid_headers = defaultdict(list)

    # skip all patches that are not contained by pathes to run
    patches_to_skip = [cocci_patch for cocci_patch in CocciPatch if cocci_patch not in patches_to_run]
    
    all_atoms = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for file_name, added in added_lines.items():
            added_line_numbers = [line.new_lineno for line in added]

            atoms = run_coccinelle_for_file_at_commit(
                repo, file_name, commit, added_line_numbers, temp_dir, loaded_headers, invalid_headers, patches_to_skip)
            for atom in atoms:
                all_atoms.append({
                    "atom_name": atom[0],
                    "file": atom[1],
                    "start_row": int(atom[2]),
                    "start_col": int(atom[3]),
                    "code": atom[6]
                })

    return all_atoms

def find_removed_atoms(repo, atoms_data, output_file, last_processed_file):       
 
    last_processed_commit = None
    last_processed = {}
    if last_processed_file.is_file():
        last_processed = json.loads(last_processed_file.read_text())
        if last_processed:
            last_processed_commit = last_processed["commit"]
    
        
    found_first = None
    for commit_sha, commit_data in atoms_data.items():
        if last_processed_commit and not found_first:
            if commit_sha == last_processed_commit:
                found_first = True
            continue

        print(f"Current commit {commit_sha}")
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
        
        # should probably analyze added lines that are linked with removed lines
        lines_map = map_similar_lines(removed_lines_with_atoms, added_lines)
        # find removed lines atoms

        if lines_map:
            patches = set()
            added_files_map = defaultdict(list)
            removed_atoms = defaultdict(list)
            for file_removed_diff, added in lines_map.items():
                similarity_index = added[1]
                if similarity_index == 1:
                    continue
                file, removed_diff = file_removed_diff
                for atom_data  in commit_data:
                    if atom_data["file"] == file and atom_data["start_row"] == removed_diff.old_lineno:
                        atom_name = atom_data["atom_name"]
                        patches.add(atom_name_to_patch_mapping[atom_name])
                        removed_atoms[removed_diff].append(atom_data)
      
                added_files_map[file].append(added[0])
            
            if len(patches):
                added_atoms = find_atoms_added_lines(added_files_map, commit, patches)
                for file_removed_diff, added in lines_map.items():
                    added_diff = added[0]
                    file, removed_diff = file_removed_diff
                    if removed_diff in removed_atoms:
                        removed_atoms_data = removed_atoms[removed_diff]
                        for removed_atom in removed_atoms_data:
                            removed_and_added = False
                            for added_data in added_atoms:
                                if added_data["atom_name"] == removed_atom["atom_name"] and \
                                    added_data["start_row"] == added_diff.new_lineno:
                                    removed_and_added = True
                                    break
                            if not removed_and_added:
                                atoms_diff.append([
                                    removed_atom["atom_name"],
                                    removed_atom["file"],
                                    removed_atom["commit"],
                                    removed_atom["start_row"],
                                    removed_atom["start_col"],
                                    removed_atom["code"]
                                ])
        append_rows_to_csv(output_file, atoms_diff)
        last_processed["commit"] = commit_sha
        last_processed_file.write_text(json.dumps(last_processed, indent=4))


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
                "code": row[5]
            }

            atoms_by_commit[data["commit"]].append(data)
        
    return atoms_by_commit

if __name__ == "__main__":
    filename = "atoms2.csv"
    repo_path = ROOT_DIR.parent / "atoms/projects/linux"  # Change this to your repo path
    output = Path("results/removed/atoms.csv")
    last_processed_file = Path("last_processed/removed/last_processed.json")
    output.parent.mkdir(exist_ok=True)
    last_processed_file.parent.mkdir(exist_ok=True)
    try:
        repo = pygit2.Repository(repo_path)
        atoms_data = read_and_sort_data(filename)
        find_removed_atoms(repo, atoms_data, output, last_processed_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
