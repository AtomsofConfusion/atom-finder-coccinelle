from asyncio import Event
from collections import defaultdict
import csv
import difflib
from functools import partial
import json
from multiprocessing import Process
import re
import tempfile
import clang
import pygit2
from pygit2.enums import DeltaStatus
from pathlib import Path
from src import ROOT_DIR
from src.run_cocci import CocciPatch, find_atoms
from clang.cindex import Index, CursorKind, Config


Config.set_library_file('/usr/lib/llvm-14/lib/libclang-14.so.1')


def is_complex_structure(cursor):
    return cursor.kind in [
        CursorKind.IF_STMT, CursorKind.FOR_STMT,
        CursorKind.WHILE_STMT,
        CursorKind.SWITCH_STMT, CursorKind.STRUCT_DECL,
    ]


def save_headers_to_temp(full_code, output_dir, repo, commit, loaded_headers, invalid_headers):

    
    _extract_headers(output_dir, full_code, repo, commit, loaded_headers, invalid_headers)



def save_all_headers(output_dir, commit, repo):
    # if it's better to save all headers, this can be used
    # doesn't seem to make a difference
    subfolder_tree = commit.tree
    subfolder_tree = repo.get(subfolder_tree["include"].id)
    _save_all_headers(output_dir, subfolder_tree, repo, path_prefix="include")

def _save_all_headers(output_dir, tree, repo, path_prefix):
    for entry in tree:
        entry_path = f"{path_prefix}/{entry.name}".strip("/")
        if entry.type == pygit2.GIT_OBJ_TREE:
            sub_tree = repo.get(entry.id)
            _save_all_headers(output_dir, sub_tree, repo, entry_path)
        elif entry.type == pygit2.GIT_OBJ_BLOB:
            header_name = f"{path_prefix.split('include/')[1]}/{entry.name}"
            path = Path(output_dir / header_name)
            file_content = entry.read_raw().decode()
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text(file_content)

def _extract_headers(output_dir, code, repo, commit, processed, invalid):
    """
    Recursively extract all unique header file names from the C code.

    :param code: C code from which to extract header files.
    :param base_path: The base directory where header files are searched (as a Path object).
    :param processed: A set to keep track of processed header files to avoid cyclic includes.
    :return: A set of all header files included in the code, directly or indirectly.
    """
    header_pattern = re.compile(r'#include\s+<([^>]+)>')
    headers = set(header_pattern.findall(code))
    all_headers = set(headers)

    for header in headers:
        if header in processed[commit] or header in invalid[commit]:
            continue
        if header not in processed[commit]:
            processed[commit].append(header)
            header_name = str(Path("include", header))
            try:
                file_content = get_file_content_at_commit(repo, commit, header_name)
                path = Path(output_dir / header)
                path.parent.mkdir(exist_ok=True, parents=True)
                path.write_text(file_content)
            except Exception as e:
                print(f"Cannot load {header} at {commit} due to {e}")
                invalid[commit].append(header)
                continue
            included_headers = _extract_headers(output_dir, file_content, repo, commit, processed, invalid)
            all_headers.update(included_headers)
    return all_headers


def parse_and_modify_functions(code, removed_line_numbers, include_dir, file_name):
    index = Index.create()
    tu = index.parse(file_name, args=['-std=c11', '-nostdinc', f"-I{include_dir}"], unsaved_files=[(file_name, code)])
    
    lines = code.splitlines()

    def prepare_modifications(cursor, removed_line_numbers):
        for child in cursor.get_children():
            if child.location.file and file_name not in child.location.file.name:
                continue
            is_function = child.kind == CursorKind.FUNCTION_DECL
            is_complex = is_complex_structure(child)
            continue_inner_search = True
            if is_function or is_complex:
                start = child.extent.start.line
                end = child.extent.end.line
                lines = [line for line in range(start, end + 1)]

                any_contained = any(line in removed_line_numbers for line in lines)
                all_contained = all(line in removed_line_numbers for line in lines)

                # if all contained, the whole function was removed
                if is_function:
                    if not any_contained or all_contained:
                        # Find the compound statement that is the body of the function
                        for c in child.get_children():
                            if c.kind == CursorKind.COMPOUND_STMT:
                                # Calculate the start and end offsets for the body
                                body_start_line = c.extent.start.line
                                body_end_line = c.extent.end.line - 2
                                # Store the offsets and the count of newlines to preserve formatting
                                lines[body_start_line:body_end_line + 1] = ["" for _ in range(body_end_line - body_start_line + 1)]
                                break
                        continue_inner_search = False
                    elif not any_contained:
                        continue_inner_search = False

                if is_complex:
                    if len(lines) == 1:
                        continue
                    # print(lines)
                    # print(removed_line_numbers)
                    if all_contained:
                        for line in lines:
                            removed_line_numbers.remove(line)
                        continue_inner_search = False
                    elif not any_contained:
                        continue_inner_search = False

            if continue_inner_search:
                prepare_modifications(child, removed_line_numbers)

    modified_line_numbers = list(set(removed_line_numbers))
    prepare_modifications(tu.cursor, modified_line_numbers)
    return "\n".join(lines), modified_line_numbers


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

def append_rows_to_csv(file_path, data):
    """
    Appends rows to a CSV file. If the file does not exist, it will be created.

    Args:
    file_path (str): Path to the CSV file where data will be appended.
    data (list of lists): Data to append, where each sublist represents a row.
    """
    # Open the file in append mode ('a') and create it if it doesn't exist ('a+')
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write each row from the data list to the CSV file
        for row in data:
            writer.writerow(row)


def get_file_content_at_commit(repo, commit, file_path):
    """
    Retrieve the content of a file at a specific commit in a Git repository.

    Args:
    repo_path (str): Path to the repository.
    commit_sha (str): The SHA of the commit.
    file_path (str): Path to the file within the repository.

    Returns:
    str: Content of the file at the specified commit, or an error message if the file does not exist.
    """
    try:
        # Retrieve the entry and blob from the commit's tree
        file_entry = commit.tree[file_path]
        blob = repo.get(file_entry.id)
        return blob.data.decode('utf-8')  # Assuming the file content is text and utf-8 encoded
    except KeyError:
        return "File not found in the specified commit."


def run_with_process_timeout(task, timeout):
    stop_event = Event()
    process = Process(target=task)
    process.start()
    process.join(timeout)
    if process.is_alive():
        print("Process did not complete within timeout.")
        stop_event.set()
        process.terminate()  # Forcefully terminate the process
        process.join()
        return False
    return True


def find_removed_atoms(repo, commit):
    """
    Get removed lines (lines removed in a commit) by comparing the commit to its parent.
    """
    PATCHES_TO_SKIP = [CocciPatch.OMITTED_CURLY_BRACES]

    parent = commit.parents[0]
    diff = repo.diff(parent, commit, context_lines=0, interhunk_lines=0)
    print(f"Current commit: {commit.hex}")
    atoms = []

    added_lines = defaultdict(list)
    removed_lines = defaultdict(list)
    for patch in diff:
        status = patch.delta.status
        if status != DeltaStatus.MODIFIED:
            continue
        file_name = patch.delta.new_file.path
        if Path(file_name).suffix not in (".c", ".h"):
            continue

        for hunk in patch.hunks:
            for line in hunk.lines:
                if line.old_lineno != -1:
                    removed_lines[file_name].append(line)
                if line.new_lineno != -1:
                    added_lines[file_name].append(line)

    if removed_lines:
        line_numbers_per_files = {}
        loaded_headers = defaultdict(list)
        invalid_headers = defaultdict(list)
        with tempfile.TemporaryDirectory() as temp_dir:
            headers_dir = Path(temp_dir, "headers")
            line_mapping = map_similar_lines(removed_lines, added_lines)
            # for removed_pair, added_pair in line_mapping.items():
            #     print(removed_pair[1].content)
            #     print(added_pair[0].content)
            #     print(added_pair[1])
            #     print("--------")
            for file_name, removed in removed_lines.items():
                removed_line_numbers = [line.old_lineno for line in removed]
                content = get_file_content_at_commit(repo, parent, file_name)
                save_headers_to_temp(
                    commit=parent,
                    output_dir=headers_dir,
                    repo=repo,
                    full_code=content,
                    loaded_headers=loaded_headers,
                    invalid_headers=invalid_headers
                )
                shorter_content, modified_lines = parse_and_modify_functions(
                    content, removed_line_numbers, headers_dir, file_name)

                line_numbers_per_files[file_name] = modified_lines

                # Define file paths within the temporary directory
                input = Path(temp_dir, "input", file_name)
                input.parent.mkdir(parents=True, exist_ok=True)
                input.write_text(shorter_content)


            # for now, remove lines with similarity index 1
            for removed, similarity_data in line_mapping.items():
                _, similarity = similarity_data
                if similarity == 1:
                    file_name, r_line = removed
                    line_no = r_line.old_lineno
                    if line_no in line_numbers_per_files[file_name]:
                        line_numbers_per_files[file_name].remove(line_no)

            output = Path(temp_dir, 'output.csv')
            input_dir = Path(temp_dir, "input")
            # now, run coccinelle patches

            task = partial(find_atoms, input_dir, output, None, PATCHES_TO_SKIP)
            if run_with_process_timeout(task,  300 ):
                with open(output, mode="r", newline="") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) == 1:
                            continue
                        atom, path, start_line, start_col, end_line, end_col, code = row
                        file_name = path.split(f"{input_dir}/")[1]
                        if int(start_line) in line_numbers_per_files[file_name]:
                            row[1] = file_name
                            output_row = [atom, file_name, commit.hex, start_line, start_col, code]
                            atoms.append(output_row)
    return atoms
    

def iterate_commits_and_extract_removed_code(repo_path, stop_commit):
    """
    Iterate through commits, check commit message, and retrieve removed code if condition is met.
    Stop iteration when the stop_commit is reached.
    
    Args:
        repo_path (str): Path to the repository.
        stop_commit (str): SHA of the commit where the iteration should stop.
        sha_condition (str): Pattern to match 'Fixes: <sha>'.
    """
    repo = pygit2.Repository(repo_path)
    head = repo.head.target  # Get the HEAD commit

    # Regular expression to match 'Fixes: <SHA>'
    fixes_pattern = re.compile(r"Fixes:\s+([0-9a-fA-F]{6,12})", re.IGNORECASE)

    commit_fixes = []

    stop_iteration = False
    for commit in repo.walk(head, pygit2.GIT_SORT_TIME):
        commit_message = commit.message.strip()

        # make sure the last pair is added
        if stop_iteration:
            break

        # Check the condition using the regex
        if fixes_pattern.search(commit_message):
            commit_fixes.append(commit.hex)

        # Stop when the specific commit is reached
        if str(commit.hex) == stop_commit:
            stop_iteration = True        

    Path("commits.json").write_text(json.dumps(commit_fixes))


def get_removed_lines(repo_path, commits):
    repo = pygit2.Repository(repo_path)
    output = Path("./atoms.csv")
    processed_path = Path("./last_processed.json")
    processed = {}
    if processed_path.is_file():
        processed = json.loads(processed_path.read_text())

    count = processed.get("count", 0)
    count_w_atoms = processed.get("count_w_atoms", 0)
    # first_commit = processed.get("last_commit")
    first_commit = None

    found_first_commit = first_commit is None
    for commit_sha in commits:
        if first_commit and commit_sha == first_commit:
            found_first_commit = True
            # alreadt processed, skip
            continue
        if not found_first_commit:
            continue
        commit = repo.get(commit_sha)
        try:
            atoms = find_removed_atoms(repo, commit)
            count += 1
            if atoms:
                append_rows_to_csv(output, atoms)
                count_w_atoms += 1
                print(f"Count with atoms: {count_w_atoms}")
            print(f"Total count: {count}")
        except Exception as e:
            print(e)
            continue
        processed = {
            "count": count,
            "count_w_atoms": count_w_atoms,
            "last_commit": commit.hex
        }
        processed_path.write_text(json.dumps(processed))
        

if __name__ == "__main__":
    # Example usage
    repo_path = ROOT_DIR.parent / "atoms/projects/linux"  # Change this to your repo path
    stop_commit = "c511851de162e8ec03d62e7d7feecbdf590d881d"  # Replace with the commit SHA to stop at
    # iterate_commits_and_extract_removed_code(repo_path, stop_commit)

    commits = json.loads(Path("commits.json").read_text())
    commits = ["6422cde1b0d5a31b206b263417c1c2b3c80fe82c"]
    get_removed_lines(repo_path, commits)
