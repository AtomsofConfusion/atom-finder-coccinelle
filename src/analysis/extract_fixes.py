from collections import defaultdict
import csv
import json
import re
import tempfile
import pygit2
from pathlib import Path
from src import ROOT_DIR
from src.run_cocci import find_atoms


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
            print(temp_dir)
            for file_name, removed in removed_lines.items():
                line_numbers = [line.old_lineno for line in removed]
                line_numbers_per_files[file_name] = line_numbers
                content = get_file_content_at_commit(repo, parent, file_name)
                if len(content.splitlines()) > 1000:
                    # for now, skip larger files
                    continue
                # Define file paths within the temporary directory
                input = Path(temp_dir, file_name)
                input.parent.mkdir(parents=True, exist_ok=True)
                input.write_text(content)

            output = Path(temp_dir, 'output.csv')

            # now, run coccinelle patches
            print("finding atoms")
            find_atoms(temp_dir, output)
            print("done")
            with open(output, mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 1:
                        continue
                    atom, path, start_line, start_col, end_line, end_col, code = row

                    file_name = path.split(f"{temp_dir}/")[1]
                    if start_line in line_numbers_per_files[file_name]:
                        row[1] = file_name
                        print(row)
    

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
    for commit_sha in commits:
        commit = repo.get(commit_sha)
        find_removed_atoms(repo, commit)

if __name__ == "__main__":
    # Example usage
    repo_path = ROOT_DIR.parent / "atoms/projects/linux"  # Change this to your repo path
    stop_commit = "c511851de162e8ec03d62e7d7feecbdf590d881d"  # Replace with the commit SHA to stop at
    # iterate_commits_and_extract_removed_code(repo_path, stop_commit)

    commits = json.loads(Path("commits.json").read_text())
    get_removed_lines(repo_path, commits)
