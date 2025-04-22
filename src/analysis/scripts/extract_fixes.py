from collections import defaultdict
import csv
import json
import multiprocessing
import re
import tempfile
import pygit2
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..')))
from src import ROOT_DIR
from src.analysis.utils.parsing import run_coccinelle_for_file_at_commit
from src.analysis.utils.git import get_diff
from src.analysis.utils.utils import append_rows_to_csv, append_to_json, safely_load_json
from src.run_cocci import CocciPatch
from src.log import logger


PATCHES_TO_SKIP = [CocciPatch.OMITTED_CURLY_BRACES]
REPO_PATH = (ROOT_DIR.parent.parent / "linux").absolute()  # Path to the Linux kernel Git repository "atoms/projects/linux").absolute()
COMMITS_FILE_PATH = Path("../commits.json")  # Path to a JSON file containing commit hashes
RESULTS_DIR = Path("../results")
LAST_PROCESSED_DIR = Path("../last_processed")
ERRORS_FILE_DIR = RESULTS_DIR/ "extract"
NUMBER_OF_PROCESSES = 5


def find_removed_atoms(repo, commit):
    """
    Get removed lines (lines removed in a commit) by comparing the commit to its parent.
    """
    logger.info(f"Current commit: {str(commit.id)}")
    atoms = []

    _, removed_lines = get_diff(repo, commit)

    if removed_lines:
        loaded_headers = defaultdict(list)
        invalid_headers = defaultdict(list)

    parent = commit.parents[0]
    output = []
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        for file_name, removed in removed_lines.items():
            removed_line_numbers = [line.old_lineno for line in removed]
            print(f"Removed lines in {file_name}: {removed_line_numbers}", type(temp_dir))
            atoms = run_coccinelle_for_file_at_commit(
                repo,
                file_name,
                parent,
                removed_line_numbers,
                temp_dir,
                loaded_headers,
                invalid_headers,
                PATCHES_TO_SKIP,
            )

            for row in atoms:
                atom, path, start_line, start_col, end_line, end_col, code = row
                output_row = [atom, file_name, str(commit.id), start_line, start_col, code]
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
            commit_fixes.append(str(commit.id))

        # Stop when the specific commit is reached
        if str(str(commit.id)) == stop_commit:
            stop_iteration = True

    Path(COMMITS_FILE_PATH).write_text(json.dumps(commit_fixes))


def load_processed_data(processed_path):
    """Load processed data from a JSON file."""
    if processed_path.is_file():
        return json.loads(processed_path.read_text())
    return {"count": 0, "count_w_atoms": 0, "last_commit": None}


def get_removed_lines(repo_path, commits, output, processed_path, errors_path):
    """Process commits and extract lines removed in each commit."""
    repo = pygit2.Repository(str(repo_path))
    processed = load_processed_data(processed_path)
    count, count_w_atoms = processed["count"], processed["count_w_atoms"]
    first_commit = processed["last_commit"]
    found_first_commit = first_commit is None

    for commit_sha in commits:
        if first_commit and not found_first_commit:
            found_first_commit = commit_sha == first_commit
            continue
        if not found_first_commit:
            continue
        try:
            commit = repo.get(commit_sha)
            atoms = find_removed_atoms(repo, commit)
            count += 1
            if atoms:
                append_rows_to_csv(output, atoms)
                count_w_atoms += 1
            logger.info(f"Processed {count} commits, {count_w_atoms} with atoms.")
        except Exception as e:
            logger.error(e)
            append_to_json(errors_path, {"commit_sha": commit_sha, "error": str(e)})
            continue
        processed.update({"count": count, "count_w_atoms": count_w_atoms, "last_commit": str(commit.id)})
        processed_path.write_text(json.dumps(processed))


def execute(repo_path, commits, number_of_processes, results_dir, last_procesed_dir, errors_dir):
    """
    Main function to spawn the processes.
    """
    # Create a pool of worker processes
    chunks = chunkify(commits, number_of_processes)
    with multiprocessing.Pool(processes=number_of_processes) as pool:
        # Create a list of tuples, each containing arguments for task_function
        tasks = []
        for i in range(number_of_processes):
            tasks.append((repo_path, chunks[i], results_dir / f"atoms{i+1}.csv", last_procesed_dir / f"last_processed{i+1}.json",  errors_dir / f"errors{i+1}.json"))
        # Use starmap to pass multiple arguments to the task function
        pool.starmap(get_removed_lines, tasks)


def chunkify(lst, n):
    """
    Divide the input list into n chunks.
    """
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)]


def combine_results():
    results_folder = RESULTS_DIR

    combined_file_path = results_folder / "atoms.csv"

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

    stop_commit = "c511851de162e8ec03d62e7d7feecbdf590d881d" # this is the commit when the fix: convention was introduced
    commits = safely_load_json(COMMITS_FILE_PATH)
    if not commits or commits[-1] != stop_commit:
        iterate_commits_and_extract_removed_code(REPO_PATH, stop_commit)

    LAST_PROCESSED_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)
    ERRORS_FILE_DIR.parent.mkdir(exist_ok=True)

    commits = json.loads(Path(COMMITS_FILE_PATH).read_text())
    # commits = ["e589f9b7078e1c0191613cd736f598e81d2390de"]

    if len(commits) == 1 or NUMBER_OF_PROCESSES == 1:
        get_removed_lines(REPO_PATH, commits, RESULTS_DIR / "atoms.csv", LAST_PROCESSED_DIR / "last_processed.json", ERRORS_FILE_DIR / "errors.json")
    else:
        execute(REPO_PATH, commits, NUMBER_OF_PROCESSES, RESULTS_DIR, LAST_PROCESSED_DIR, ERRORS_FILE_DIR)

    combine_results()
