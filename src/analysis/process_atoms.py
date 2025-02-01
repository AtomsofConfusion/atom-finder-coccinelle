from collections import defaultdict
import csv
import difflib
import json
from pathlib import Path
import re
import pycparser
import tempfile

import pygit2

from src import ROOT_DIR
from src.analysis.parsing import contains_expression, get_function_or_statement_context, parse_file, run_coccinelle_for_file_at_commit
from src.analysis.git import get_diff, get_file_content_at_commit
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



def parse_code_to_ast(code):
    parser = pycparser.CParser()
    # Wrap the code in a complete function (use int return type for simplicity)
    full_code = f"int temp_func() {{ {code} ; }}"
    
    try:
        # Parse the full code and get the root of the AST
        ast = parser.parse(full_code)
        
        # If the root of the AST is a tuple, extract the first item (the root of the AST)
        if isinstance(ast, tuple):  
            ast = ast[0]
        
        # Check if the root node is a function definition
        if isinstance(ast, pycparser.c_ast.FileAST):
            # The root node is FileAST, and we need to extract the FuncDef from it
            func_def = ast.ext[0]  # Assuming there's only one function definition
            return func_def.body  # Return the body of the function (the block of code inside {})

    except Exception as e:
        print(f"Parsing error: {e}")
        return None

def compare_ast_structures(r_ast, a_ast):
    """
    Compare the AST structure of two code snippets.
    This is a basic comparison that checks whether the ASTs have the same structure.
    A more advanced approach could involve traversing the trees and comparing specific nodes.
    """
    if not r_ast or not a_ast:
        return 0.0

    # Compare root node types
    if r_ast.__class__ != a_ast.__class__:
        return 0.0
    # If it's a terminal node (no children), compare the actual content (e.g., the value of the node)
    if isinstance(r_ast, (pycparser.c_ast.ID, pycparser.c_ast.Constant, pycparser.c_ast.IdentifierType, pycparser.c_ast.TypeDecl, pycparser.c_ast.FuncDecl, pycparser.c_ast.FuncDecl)):
        return 1.0 if str(r_ast) == str(a_ast) else 0.0

    # If it's a non-terminal node, compare the children
    if hasattr(r_ast, 'children') and hasattr(a_ast, 'children'):
        children_r = r_ast.children()  # Get all children of r_ast
        children_a = a_ast.children()  # Get all children of a_ast
        if len(children_r) != len(children_a):
            return 0.0
        # Recursively compare children (basic approach)
        child_similarity = 0
        for (r_child_name, r_child), (a_child_name, a_child) in zip(children_r, children_a):
            child_similarity += compare_ast_structures(r_child, a_child)
        return child_similarity / max(len(children_r), 1)  # Normalize by number of children

    return 0.0


def compare_code_structure(r_line_content, a_line_content):
    r_ast = parse_code_to_ast(r_line_content)
    a_ast = parse_code_to_ast(a_line_content)
    if r_ast and a_ast:
        return compare_ast_structures(r_ast, a_ast)
    return 0.0  # If parsing fails, return 0.0 similarity


def group_consecutive_lines(line_map):
    grouped_lines = {}
    for (file, line), match in line_map.items():
        if file not in grouped_lines:
            grouped_lines[file] = []
        
        current_group = grouped_lines[file]
        if not current_group or current_group[-1][-1][0].old_lineno != line.old_lineno - 1:
            current_group.append([])  # Start a new group
        
        current_group[-1].append((line, match))

    return grouped_lines

def map_similar_lines(removed, added):

    def _calculate_combined_score(r_line, a_line, max_line_distance):
        similarity = difflib.SequenceMatcher(None, r_line.content.strip(), a_line.content.strip()).ratio()
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
        current_best = assigned_added.get(a_line, (None, 0))  # Get current best match and its score

        # If the current line has a better match or if the added line is not yet assigned
        if score > current_best[1]:
            if current_best[0] is not None:
                # Previous match is superseded, remove the previous best match
                del best_matches[(r_file, current_best[0])]
            # Assign the new best match
            best_matches[(r_file, r_line)] = (a_line, score)
            assigned_added[a_line] = (r_line, score)
        elif a_line not in assigned_added:
            # If the added line is not yet used, assign it
            best_matches[(r_file, r_line)] = (a_line, score)
            assigned_added[a_line] = (r_line, score)

    return best_matches


def find_atoms_added_lines(temp_dir, added_lines, commit, patches_to_run):
    loaded_headers = defaultdict(list)
    invalid_headers = defaultdict(list)

    # skip all patches that are not contained by pathes to run
    patches_to_skip = [cocci_patch for cocci_patch in CocciPatch if cocci_patch not in patches_to_run]
    
    all_atoms = []

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
    processed_pairs = defaultdict(list)

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

            grouped_lines = group_consecutive_lines(lines_map)
            for file, groups in grouped_lines.items():
                pass
            patches = set()
            added_files_map = defaultdict(list)
            removed_atoms = defaultdict(list)
            for file_removed_diff, added in lines_map.items():
                added_diff, similarity_index = added
                if similarity_index == 1:
                    # lines are identical, there is no point in analyzing
                    continue
                file, removed_diff = file_removed_diff
                removed_content = removed_diff.content.strip()
                added_content = added_diff.content.strip()
                if added_content in processed_pairs.get(removed_content, []):
                    print("Pair already processed")
                    continue
                processed_pairs[removed_content].append(added_content)

                for atom_data  in commit_data:
                    if atom_data["file"] == file and atom_data["start_row"] == removed_diff.old_lineno:
                        atom_name = atom_data["atom_name"]
                        patches.add(atom_name_to_patch_mapping[atom_name])
                        removed_atoms[removed_diff].append(atom_data)
      
                added_files_map[file].append(added[0])
            
            if len(patches):
                with tempfile.TemporaryDirectory() as temp_dir:
                    added_atoms = find_atoms_added_lines(temp_dir, added_files_map, commit, patches)
                    for file_removed_diff, added in lines_map.items():
                        added_diff = added[0]
                        file, removed_diff = file_removed_diff
                        current_atoms_diff = []
                        if removed_diff in removed_atoms:
                            removed_atoms_data = removed_atoms[removed_diff]
                            for removed_atom in removed_atoms_data:
                                removed_and_added = False
                                for added_data in added_atoms:
                                    atom_name = removed_atom["atom_name"]
                                    if added_data["atom_name"] == atom_name and \
                                        added_data["start_row"] == added_diff.new_lineno:
                                        removed_and_added = True
                                        break
                                if not removed_and_added:
                                    if update_of_interest(removed_diff, added_diff, atom_name):
                                        current_atoms_diff.append([
                                            atom_name,
                                            removed_atom["file"],
                                            removed_atom["commit"],
                                            removed_atom["start_row"],
                                            removed_atom["start_col"],
                                            added_diff.new_lineno,
                                            removed_atom["code"],
                                        ])
                        current_atoms_diff = filter_atoms(current_atoms_diff)
                        atoms_diff.extend(current_atoms_diff) 
        append_rows_to_csv(output_file, atoms_diff)
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


def extract_if_condition(code):
    # Pattern to find 'if' followed by any characters until the first '('
    if_pattern = r'\bif\s*\('
    match = re.search(if_pattern, code)
    if not match:
        return code  # Return original if no 'if(' is found

    # Find the matching closing parenthesis for the 'if'
    start_index = match.end() - 1  # Position of the opening '('
    end_index = find_matching_parenthesis(code, start_index)
    if end_index == start_index:
        return code  # No matching ')' found, return original or handle error

    # Extract the content inside the parentheses
    condition = code[start_index + 1:end_index].strip()
    return condition

def find_matching_parenthesis(code, start_index):
    """ Find the index of the matching parenthesis starting from just after 'if(' """
    open_paren = 1 
    for i in range(start_index + 1, len(code)):
        if code[i] == "(":
            open_paren += 1
        elif code[i] == ")":
            open_paren -= 1
        if open_paren == 0:
            return i
    return start_index  
   
def check_if_parentheses_added(removed_diff, added_diff):
    # I'd like to parse this and use clang to compare the lines
    # however, there are occasional parsing issues (probably something missing)

    def count_operators_and_parentheses(code):
        # Remove strings (both single and double quoted)
        code_without_strings = re.sub(r'".*?"|\'.*?\'', '', code)

        # Remove single-line and multi-line comments
        code_clean = re.sub(r'//.*?$|/\*.*?\*/', '', code_without_strings, flags=re.DOTALL | re.MULTILINE)

        # Define regex patterns for unary and binary operators
        unary_operators = [
            r'\b\+\+', r'\b--',  # Increment and decrement
            r'(?<!\w)!(?=\s*\()', # Logical NOT directly followed by an opening parenthesis with optional whitespace
            r'(?<!\w)!(?=\s*\w)', # Logical NOT directly followed by a word character with optional whitespace
            r'(?<=\()\s*-\s*(?=\d|\w)' # Negative numbers or negation directly after an opening parenthesis
        ]
        binary_operators = [
            r'(?<!\+)\+(?!\+)', r'(?<!-)-(?!-)', r'\*', r'/', r'%', 
            r'==', r'!=', r'<=', r'>=', r'&&', r'\|\|', 
            r'&(?!\&)', r'\|(?!\|)', r'\^', r'<<', r'>>', 
            r'(?<!<)<(?!<)', r'(?<!>)>(?!>)'
        ]
        parentheses = [r'\(', r'\)']

        # Count occurrences
        counts = {
            "unary": sum(len(re.findall(pattern, code_clean)) for pattern in unary_operators),
            "binary": sum(len(re.findall(pattern, code_clean)) for pattern in binary_operators),
            "parentheses": sum(len(re.findall(pattern, code_clean)) for pattern in parentheses)
        }

        return counts
    
    removed_counts = count_operators_and_parentheses(removed_diff.content)
    added_counts = count_operators_and_parentheses(added_diff.content)
    # this isn't very robust at all
    # need to parse, but figure out parsing issues first
    return removed_counts["unary"] == added_counts["unary"] and \
        removed_counts["binary"] == added_counts["binary"] and \
        removed_counts["parentheses"] < added_counts["parentheses"]


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
