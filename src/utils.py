import csv
import io

def append_to_csv(file_path, data):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        for row in data:
            parsed_row = next(csv.reader([row]))
            writer.writerow(parsed_row)


def parse_csv_data(data):
    # Use StringIO to convert string data into a file-like object for csv.reader
    data_io = io.StringIO(data)
    reader = csv.reader(data_io)
    return list(reader)
    

def write_to_csv(file_path, data):
    with open(file_path, mode="w", newline='') as file:
        writer = csv.writer(file)
        for row in data:
            parsed_row = next(csv.reader([row]))
            writer.writerow(parsed_row)
