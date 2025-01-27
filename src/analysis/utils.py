import csv
import json


def append_rows_to_csv(file_path, data):
    """
    Appends rows to a CSV file. If the file does not exist, it will be created.

    Args:
    file_path (str): Path to the CSV file where data will be appended.
    data (list of lists): Data to append, where each sublist represents a row.
    """
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        for row in data:
            writer.writerow(row)


def append_to_json(json_file, item):
    if not json_file.exists():
        data = []
    else:
        with json_file.open('r') as file:
            data = json.load(file)

    data.append(item)

    with json_file.open('w') as file:
        json.dump(data, file, indent=4)