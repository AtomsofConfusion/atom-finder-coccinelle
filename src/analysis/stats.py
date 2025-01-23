import csv
from collections import Counter
import datetime
import json
from pathlib import Path

def count_atoms_occurrences(filename):
    counts = Counter()

    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        
        for row in reader:
            if row:
                atoms = row[0]
                counts[atoms] += 1

    return counts

# filename = "atoms.csv"
# result = count_atoms_occurrences(filename)
# print(result)
# total = sum(result.values())
# print(f"Total: {total}")


folder_path = Path('last_processed')

total_count = 0
total_count_w_atoms = 0

for file_path in folder_path.iterdir():
    if file_path.is_file() and file_path.suffix == '.json':
        # Open and read the JSON file
        with file_path.open('r') as file:
            data = json.load(file)
            count = data.get('count', 0)
            count_w_atoms = data.get('count_w_atoms', 0)
            
            total_count += count
            total_count_w_atoms += count_w_atoms


current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Total count: {total_count}")
print(f"Total count with atoms: {total_count_w_atoms}")
print(f"Current time: {current_time}")
