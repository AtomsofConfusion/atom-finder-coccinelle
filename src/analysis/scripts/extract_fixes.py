from collections import defaultdict
import csv
import json
import multiprocessing
import re
import tempfile
import pygit2
import time
from pathlib import Path
from timelength import TimeLength
from src import ROOT_DIR
from src.analysis.utils.parsing import run_coccinelle_for_file_at_commit
from src.analysis.utils.git import get_diff
from src.analysis.utils.utils import append_rows_to_csv, append_to_json, safely_load_json
from src.run_cocci import CocciPatch
from src.log import logger

PATCHES_TO_SKIP = [CocciPatch.OMITTED_CURLY_BRACES]

def find_removed_atoms(repo, commit):
    """
    Get removed lines (lines removed in a commit) by comparing the commit to its parent.
    """
    logger.info(f"Current commit: {commit.id}")
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


def iterate_commits_and_extract_removed_code(repo_path, stop_commit, commits_file_path ,history_length = None):
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

    # Calculate cutoff timestamp if history_length is provided
    cutoff_timestamp = None
    if history_length is not None:
        tl = TimeLength(history_length)
        now = int(time.time())
        cutoff_timestamp = now - int(tl.to_minutes()*60)


    commit_fixes = []

    stop_iteration = False
    for commit in repo.walk(head, pygit2.GIT_SORT_TIME):
        commit_message = commit.message.strip()
        #print(commit.id)

        # Filter by cutoff timestamp if set
        if cutoff_timestamp is not None and commit.commit_time < cutoff_timestamp:
            break

        # make sure the last pair is added
        if stop_iteration:
            break

        # Check the condition using the regex
        if fixes_pattern.search(commit_message):
            commit_fixes.append(str(commit.id))

        # Stop when the specific commit is reached
        if str(commit.id) == stop_commit:
            stop_iteration = True

    commits_file_path.write_text(json.dumps(commit_fixes))


def load_processed_data(processed_path):
    """Load processed data from a JSON file."""
    if processed_path.is_file():
        return json.loads(processed_path.read_text())
    return {"count": 0, "count_w_atoms": 0, "last_commit": None}


'''
Single thread version 
'''
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

'''
Mutliprocessing using static commit lists
'''
def execute(repo_path, commits, number_of_processes, results_dir, last_procesed_dir, errors_dir):
    """
    Main function to spawn the processes.
    """
    if not number_of_processes:
        number_of_processes = multiprocessing.cpu_count()
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


def _get_removed_lines_worker(repo_path, commit_queue, output, processed_path, errors_path):
    """
    Worker function that pulls commits from the shared queue.
    """
    repo = pygit2.Repository(str(repo_path))
    processed = load_processed_data(processed_path)
    count, count_w_atoms = processed["count"], processed["count_w_atoms"]
    first_commit = processed["last_commit"]
    found_first_commit = first_commit is None

    while True:
        try:
            commit_sha = commit_queue.get_nowait()
        except Exception:
            break  # Queue is empty

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


def execute_queue(repo_path, commits, number_of_processes, results_dir, last_procesed_dir, errors_dir):
    '''
    Multiprocessing using shared queue of commits 

    Args:
        repo_path (str): Path to the repository.
        commits (list[str]): list of commits to be processed
        number_of_processes (int): number of worker processes to use
        *_dir (path): output directories 
    '''
    if not number_of_processes:
        number_of_processes = multiprocessing.cpu_count()

    manager = multiprocessing.Manager()
    commit_queue = manager.Queue()
    for commit in commits:
        commit_queue.put(commit)

    processes = []
    for i in range(number_of_processes):
        p = multiprocessing.Process(
            target=_get_removed_lines_worker,
            args=(
                repo_path,
                commit_queue,
                results_dir / f"atoms{i+1}.csv",
                last_procesed_dir / f"last_processed{i+1}.json",
                errors_dir / f"errors{i+1}.json",
            ),
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

'''
Combines multiprocessing results into single data set
'''
def combine_results(results_folder):

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

