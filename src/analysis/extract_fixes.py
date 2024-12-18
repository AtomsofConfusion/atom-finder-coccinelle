from collections import defaultdict
import json
import re
import tempfile
import pygit2
from pathlib import Path
from src import ROOT_DIR
from src.run_cocci import find_atoms, run_cocci


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


def get_removed_lines_from_diff(repo, commit, previous_commit):
    """
    Get removed lines (lines removed in a commit) by comparing the commit to its parent.
    """

    diff = repo.diff(previous_commit, commit)

    removed_lines = defaultdict(list)
    for patch in diff:
        file_name = patch.delta.new_file.path

        for hunk in patch.hunks:
            for line in hunk.lines:
                if line.old_lineno != -1:
                    removed_lines[file_name].append(line)
    
    if removed_lines:
        for file_name, removed in removed_lines.items():
            content = get_file_content_at_commit(repo, previous_commit, file_name)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', encoding='utf-8') as tmpfile:
                tmpfile.write(content)
                temp_file_path = tmpfile.name  # Store the path to the temporary file
                # now, run coccinelle patches
                atoms = find_atoms(temp_file_path)
                import pdb; pdb.set_trace()
    

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


    current_pair = {}
    stop_iteration = False
    for commit in repo.walk(head, pygit2.GIT_SORT_TIME):
        commit_message = commit.message.strip()
        if len(current_pair):
            current_pair["previous"] = commit.hex
            commit_fixes.append(current_pair)
            current_pair = {}

        # make sure the last pair is added
        if stop_iteration:
            break

        # Check the condition using the regex
        if fixes_pattern.search(commit_message):
            current_pair["commit"] = commit.hex

        # Stop when the specific commit is reached
        if str(commit.hex) == stop_commit:
            stop_iteration = True
        

    Path("commits.json").write_text(json.dumps(commit_fixes))



def get_removed_lines(repo_path, commits):
    repo = pygit2.Repository(repo_path)
    for commit_and_previous in commits:
        commit_sha = commit_and_previous["commit"]
        previous_sha = commit_and_previous["previous"]
        commit = repo.get(commit_sha)
        previous = repo.get(previous_sha)
        removed_lines = get_removed_lines_from_diff(repo, commit, previous)
        print("Removed lines:")
        for line in removed_lines:
            print(f"- {line}")
        print()

if __name__ == "__main__":
    # Example usage
    repo_path = ROOT_DIR.parent / "atoms/projects/linux"  # Change this to your repo path
    stop_commit = "c511851de162e8ec03d62e7d7feecbdf590d881d"  # Replace with the commit SHA to stop at
    # iterate_commits_and_extract_removed_code(repo_path, stop_commit)

    commits = json.loads(Path("commits.json").read_text())
    get_removed_lines(repo_path, commits)