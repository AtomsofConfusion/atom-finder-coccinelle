from collections import defaultdict
import csv
import json
import re
import tempfile
import pygit2
from pathlib import Path
from src import ROOT_DIR
from src.run_cocci import find_atoms
from clang.cindex import Index, CursorKind, Config


Config.set_library_file('/usr/lib/llvm-14/lib/libclang-14.so.1')

def parse_and_modify_functions(code, removed_line_numbers):
    index = Index.create()
    tu = index.parse('dummy.c', args=['-std=c11'], unsaved_files=[('dummy.c', code)])
    
    lines = code.splitlines()

    def prepare_modifications(cursor, removed_line_numbers):
        for child in cursor.get_children():
            if child.kind == CursorKind.FUNCTION_DECL:
                function_start = child.extent.start.line
                function_end = child.extent.end.line
                function_lines = [line for line in range(function_start, function_end + 1)]

                any_contained = any(line in  removed_line_numbers for line in function_lines)
                all_contained = all(line in  removed_line_numbers for line in function_lines)

                # if all contained, the whole function was removed
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
            prepare_modifications(child, removed_line_numbers)

    prepare_modifications(tu.cursor, set(removed_line_numbers))

    return "\n".join(lines)


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


def find_removed_atoms(repo, commit):
    """
    Get removed lines (lines removed in a commit) by comparing the commit to its parent.
    """

    parent = commit.parents[0]
    diff = repo.diff(parent, commit, context_lines=0, interhunk_lines=0)
    print(f"Current commit: {commit.hex}")
    atoms = []

    removed_lines = defaultdict(list)
    for patch in diff:

        file_name = patch.delta.new_file.path

        for hunk in patch.hunks:
            for line in hunk.lines:
                if line.old_lineno != -1:
                    removed_lines[file_name].append(line)

    if removed_lines:
        line_numbers_per_files = {}
        with tempfile.TemporaryDirectory() as temp_dir:
            for file_name, removed in removed_lines.items():
                line_numbers = [line.old_lineno for line in removed]
                line_numbers_per_files[file_name] = line_numbers
                content = get_file_content_at_commit(repo, parent, file_name)
                shorter_content = parse_and_modify_functions(content, line_numbers)
                # Define file paths within the temporary directory
                input = Path(temp_dir, file_name)
                input.parent.mkdir(parents=True, exist_ok=True)
                input.write_text(shorter_content)

            output = Path(temp_dir, 'output.csv')

            # now, run coccinelle patches
            find_atoms(temp_dir, output)
            with open(output, mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 1:
                        continue
                    atom, path, start_line, start_col, end_line, end_col, code = row
                    file_name = path.split(f"{temp_dir}/")[1]
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
    first_commit = processed.get("last_commit")

    found_first_commit = first_commit is None
    for commit_sha in commits:
        if first_commit and commit_sha == first_commit:
            found_first_commit = True
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
    get_removed_lines(repo_path, commits)
