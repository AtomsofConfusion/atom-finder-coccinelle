from collections import defaultdict
from pathlib import Path
from pygit2.enums import DeltaStatus

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
    

def get_diff(repo, commit):
    parent = commit.parents[0]
    diff = repo.diff(parent, commit, context_lines=0, interhunk_lines=0)

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

    return added_lines, removed_lines
