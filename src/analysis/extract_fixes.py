from collections import defaultdict
import csv
import json
import multiprocessing
import re
import tempfile
import pygit2
from pathlib import Path
from src import ROOT_DIR
from src.analysis.cocci_analysis import run_coccinelle_for_file_at_commit
from src.analysis.git import get_diff
from src.analysis.utils import append_rows_to_csv, append_to_json
from src.run_cocci import CocciPatch


PATCHES_TO_SKIP = [CocciPatch.OMITTED_CURLY_BRACES]



def find_removed_atoms(repo, commit):
    """
    Get removed lines (lines removed in a commit) by comparing the commit to its parent.
    """
    print(f"Current commit: {commit.hex}")
    atoms = []

    _, removed_lines = get_diff(repo, commit)

    if removed_lines:
        loaded_headers = defaultdict(list)
        invalid_headers = defaultdict(list)
    
    parent = commit.parents[0]
    output = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for file_name, removed in removed_lines.items():
            removed_line_numbers = [line.old_lineno for line in removed]
            atoms = run_coccinelle_for_file_at_commit(
                repo, file_name, parent, removed_line_numbers, temp_dir, loaded_headers, invalid_headers, PATCHES_TO_SKIP)

            for row in atoms:
                atom, path, start_line, start_col, end_line, end_col, code = row
                output_row = [atom, file_name, commit.hex, start_line, start_col, code]
                output.append(output_row)
        
    return output
    

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


def get_removed_lines(repo_path, commits, index=0):
    repo = pygit2.Repository(repo_path)
    if index:
        output = Path(f"./results/atoms{index}.csv")
        processed_path = Path(f"./last_processed/last_processed{index}.json")
        output.parent.mkdir(exist_ok=True)
        processed_path.parent.mkdir(exist_ok=True)
    else:
        output = Path("./atoms.csv")
        processed_path = Path("./last_processed.json")
    
    errors_path = Path("./errors.json")
    processed = {}
    if processed_path.is_file():
        processed = json.loads(processed_path.read_text())

    count = processed.get("count", 0)
    count_w_atoms = processed.get("count_w_atoms", 0)
    if len(commits) == 1:
        first_commit = None
    else:
        first_commit = processed.get("last_commit")

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
            append_to_json(errors_path, commit_sha)
            continue
        processed = {
            "count": count,
            "count_w_atoms": count_w_atoms,
            "last_commit": commit.hex
        }
        processed_path.write_text(json.dumps(processed))


def execute(repo_path, commits, number_of_processes):
    """
    Main function to spawn the processes.
    """
    # Create a pool of worker processes
    chunks = chunkify(commits, number_of_processes)
    with multiprocessing.Pool(processes=number_of_processes) as pool:
       # Create a list of tuples, each containing arguments for task_function
        tasks= []
        for i in range(number_of_processes):
            tasks.append((repo_path, chunks[i], i+1))
        # Use starmap to pass multiple arguments to the task function
        pool.starmap(get_removed_lines, tasks)

def chunkify(lst, n):
    """
    Divide the input list into n chunks.
    """
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def combine_results():
    results_folder = Path("results")

    combined_file_path = results_folder / 'atoms.csv'

    with combined_file_path.open("w", newline="") as combined_file:
        writer = csv.writer(combined_file)

        for file_path in results_folder.iterdir():
            if file_path.name != combined_file_path.name:
                if file_path.is_file() and file_path.suffix == ".csv":
                    print(f"Adding {file_path.name}")
                    with file_path.open("r", newline="") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            writer.writerow(row)

if __name__ == "__main__":
    # Example usage
    number_of_processes = 5
    repo_path = ROOT_DIR.parent / "atoms/projects/linux"  # Change this to your repo path
    stop_commit = "c511851de162e8ec03d62e7d7feecbdf590d881d"  # Replace with the commit SHA to stop at
    # iterate_commits_and_extract_removed_code(repo_path, stop_commit)

    commits = json.loads(Path("commits.json").read_text())
    # commits = ["e589f9b7078e1c0191613cd736f598e81d2390de"]
    if len(commits) == 1 or number_of_processes == 1:
        get_removed_lines(repo_path, commits)
    else:
        execute(repo_path, commits, number_of_processes)
    # combine_results()
