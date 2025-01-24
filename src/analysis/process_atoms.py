from collections import defaultdict
import csv
import difflib
import tempfile

import pygit2

from src import ROOT_DIR
from src.analysis.cocci_analysis import run_coccinelle_for_file_at_commit
from src.analysis.git import get_diff


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
    patches_to_skip = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for file_name, added in added_lines.items():
            added_line_numbers = [line.old_lineno for line in added_lines]

            atoms = run_coccinelle_for_file_at_commit(
                repo, file_name, commit, added_line_numbers, temp_dir, loaded_headers, invalid_headers, patches_to_skip)

def find_removed_atoms(repo, atoms_list):
    for atom_data in atoms_list:
        atom_name = atom_data["atom-name"]
        file = atom_data["file"]
        commit_sha = atom_data["commit"]
        commit = repo[commit_sha]

        # find all atoms linked with the same file and then analyze added lines


        added_lines, removed_lines = get_diff(repo, commit)
       
        # should probably analyze added lines that are linked with removed lines
        lines_map = map_similar_lines(removed_lines, added_lines)
        


def read_csv(filename):
    
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        data_list = []
        for row in csv_reader:
            if len(row) != 6:
                raise ValueError("Row does not contain the correct number of fields")

            data = {
                "atom-name": row[0],
                "file": row[1],
                "commit": row[2],
                "start row": int(row[3]),
                "start col": int(row[4]),
                "code": row[5]
            }

            data_list.append(data)
        
        return data_list

if __name__ == "__main__":
    filename = "atoms2.csv"
    repo_path = ROOT_DIR.parent / "atoms/projects/linux"  # Change this to your repo path
    try:
        repo = pygit2.Repository(repo_path)
        mapped_data = read_csv(filename)
        find_removed_atoms(repo, mapped_data)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
