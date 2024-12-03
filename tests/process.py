from pathlib import Path
import csv


def compare_string_sets(strings1, strings2):
    set1 = set(strings1)
    set2 = set(strings2)
    return (len(set1) == len(set2)) & all(any(s1 in s2 for s1 in set1) for s2 in set2)


def remove_whitespaces_in_column(file_path, column_index=4):
    modified_rows = []

    with open(file_path, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)

        for row in reader:
            # Check if the row has enough columns
            if len(row) > column_index:
                # Remove white spaces from the specified column (fifth column)
                row[column_index] = row[column_index].replace(" ", "")
            # Append the modified row
            modified_rows.append(row)

    # Overwrite the original file with modified content
    with open(file_path, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(modified_rows)


def process_csv_files_in_folder(folder_path):
    """
    Processes all CSV files in the given folder to remove white spaces
    from the fifth column.
    """
    # Loop through all files in the folder
    for file in Path(folder_path).glob("*.csv"):
        print(f"Processing file: {file.name}")
        remove_whitespaces_in_column(file)


if __name__ == "__main__":
    folder_path = "tests/data/expected_outputs"
    # process_csv_files_in_folder(folder_path)
    expected = ["23434", "123125", "121345"]
    output = ["123125", "12134", "234345"]
    print(compare_string_sets(expected, output))
    # print(set(output)==set(expected))
