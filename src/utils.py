import csv
import io
import os
from pathlib import Path
import re
import subprocess
from typing import List, Optional
from src.log import logging
from src.config import config 
from src.exceptions import SPatchVersionError

def append_to_csv(file_path, data):
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        for row in data:
            parsed_row = next(csv.reader([row]))
            writer.writerow(parsed_row)


def check_cocci_version():
    required_version = config["tools"]["spatch"]
    output = run(["spatch", "--version"])
    match = re.search(r'spatch version (\S+)', output)
    if match:
        version = match.group(1)
        version = version.split("-")[0]
        if version != required_version:
            raise SPatchVersionError(required_version, version)
    else:
        raise SPatchVersionError(required_version, None) 


def parse_csv_data(data):
    # Use StringIO to convert string data into a file-like object for csv.reader
    data_io = io.StringIO(data)
    reader = csv.reader(data_io)
    return list(reader)


def empty_directory(dir_path: Path, files_to_keep: Optional[List[Path]]=None):
    dir_path = Path(dir_path)  # Convert str to Path
    if dir_path.exists() and dir_path.is_dir():
        for file in dir_path.iterdir():
            if file.is_file() and not file in files_to_keep:
                file.unlink()


def run(command, **kwargs):
    """Run a command and return its output.
    In order to get bytes, call this command with `raw=True` argument.
    """
    # Skip decoding
    raw = kwargs.pop("raw", False)

    try:
        options = dict(stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True, shell=True)
        if not raw:
            options.update(universal_newlines=True)

        options.update(kwargs)
        completed = subprocess.run(" ".join(command), **options)
    except subprocess.CalledProcessError as err:
        if err.stdout:
            logging.error(err.stdout)
        if err.stderr:
            logging.error(err.stderr)
        logging.error(
            "Command {} returned non-zero exit status {} with output {}",
            " ".join(command),
            err.returncode,
            err.output,
        )
        raise err


    if completed.returncode != 0:
        return None

    return completed.stdout if raw else completed.stdout.rstrip()


def write_to_csv(file_path, data):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        for row in data:
            parsed_row = next(csv.reader([row]))
            writer.writerow(parsed_row)
