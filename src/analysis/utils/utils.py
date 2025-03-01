import csv
import json
from pathlib import Path


def append_rows_to_csv(file_path, data):
    """
    Appends rows to a CSV file. If the file does not exist, it will be created.

    Args:
    file_path (str): Path to the CSV file where data will be appended.
    data (list of lists): Data to append, where each sublist represents a row.
    """
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        for row in data:
            writer.writerow(row)


def append_to_json(json_file, item):
    if not json_file.exists():
        data = []
    else:
        try:
            with json_file.open("r") as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = []

    data.append(item)

    with json_file.open("w") as file:
        json.dump(data, file, indent=4)

def safely_load_json(file_path):
    """
    Safely load JSON data from a specified file.

    Args:
        file_path (Path or str): Path to the JSON file.

    Returns:
        dict: The content of the JSON file as a dictionary.

    Raises:
        ValueError: If the JSON data is malformed.
    """
    file_path = Path(file_path)  # Ensure the file_path is a Path object
    if not file_path.exists():
        return {}  # Return an empty dictionary if the file does not exist

    try:
        with file_path.open('r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"The JSON file '{file_path}' contains invalid JSON. Detail: {e}")
    