import click
import json
#import cProfile

from pathlib import Path
from src.analysis.scripts.extract_fixes import iterate_commits_and_extract_removed_code, get_removed_lines,execute, combine_results,execute_queue
from src.analysis.utils.utils import safely_load_json
from src import ROOT_DIR

REPO_PATH = (ROOT_DIR.parent / "projects/linux").absolute()  # Path to the Linux kernel Git repository
COMMITS_FILE_PATH = Path("commits.json")  # Path to a JSON file containing commit hashes
RESULTS_DIR = Path("./results")
LAST_PROCESSED_DIR = Path("./last_processed")
ERRORS_FILE_DIR = Path("./extract")

NUMBER_OF_PROCESSES = 4

'''
aoc-linux-fixes is a tool for examining bug fix commits to the linux kernel
It runs coccinelle patches on the changes made by the bug fix to see if the removed/modified code 
contained any atoms, or was infulence by the presence of atoms.

This tool takes up to 4 arguments:
- The directory containing a clone of the linux kernel
- A directory path for output
- A length of time from now for which to process commits
- The number of worker processes to spawn
'''

@click.command()
@click.argument("linux_dir",type=Path)
@click.option("-o", "--output-dir", type=Path, default="./output")
@click.option("-t","--history_length",type=str, default=None,help="Length of commit history to analyze")
@click.option("-p","--cpus",type=int,default=None,help="number of cpus to use for multiprocessing. Defaults to cpu_count")

def extract_linux_fixes(linux_dir = REPO_PATH,output_dir = Path("./output"),history_length = None, cpus = NUMBER_OF_PROCESSES):

    stop_commit = "c511851de162e8ec03d62e7d7feecbdf590d881d" # this is the commit when the fix: convention was introduced
    output_dir.mkdir(exist_ok=True)
    commits_file_path = output_dir / "commits.json"

    commits = safely_load_json(commits_file_path)
    if not commits or commits[-1] != stop_commit:
        iterate_commits_and_extract_removed_code(linux_dir, stop_commit, commits_file_path, history_length)

    last_processed = output_dir / LAST_PROCESSED_DIR
    last_processed.mkdir(exist_ok=True)
    results_dir = output_dir/RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    errors_dir = results_dir / ERRORS_FILE_DIR
    errors_dir.mkdir(exist_ok=True)

    commits = json.loads(commits_file_path.read_text())
    # commits = ["e589f9b7078e1c0191613cd736f598e81d2390de"]

    if len(commits) == 1 or cpus == 1:
        get_removed_lines(linux_dir, commits, results_dir / "atoms.csv", last_processed / "last_processed.json", errors_dir / "errors.json")
    else:
        #execute(linux_dir, commits, cpus, results_dir, last_processed, errors_dir)
        execute_queue(linux_dir, commits, cpus, results_dir, last_processed, errors_dir)

    combine_results(results_dir)

if __name__ == "__main__":
    extract_linux_fixes(Path("../projects/linux/"), Path("./output"), "one week", NUMBER_OF_PROCESSES)
    #cProfile.run('extract_linux_fixes(Path("../projects/linux/"), Path("./output"), "one month",0)',"profile_linux_fixes" )
