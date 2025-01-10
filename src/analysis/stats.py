import csv
from collections import Counter

def count_atoms_occurrences(filename):
    counts = Counter()

    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        
        for row in reader:
            if row:
                atoms = row[0]
                counts[atoms] += 1

    return counts

filename = "atoms.csv"
result = count_atoms_occurrences(filename)
print(result)
total = sum(result.values())
print(f"Total: {total}")