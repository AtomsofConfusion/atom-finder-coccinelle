import csv
import difflib


def map_similar_lines(removed, added):
    similarity_threshold = 0.8
    mappings = {}

    for r_file, r_lines in removed.items():
        for r_line in r_lines:
            r_line_content = r_line.content.strip()
            if r_line_content in ("{", "}") or "else" in r_line_content:
                continue
            best_match = None
            best_ratio = 0
            for _, a_lines in added.items():
                for a_line in a_lines:
                    a_line_content = a_line.content.strip()
                    ratio = difflib.SequenceMatcher(None, r_line_content, a_line_content).ratio()
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_match = (a_line, best_ratio)
            
            if best_ratio > similarity_threshold:
                mappings[(r_file, r_line)] = best_match

            # if best_match:
            #     added[r_file].remove(best_match[0]) 
    
    return mappings


def read_csv(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        data_list = []
        for row in csv_reader:
            if len(row) != 6:
                raise ValueError("Row does not contain the correct number of fields")

            data = {
                'atom-name': row[0],
                'file': row[1],
                'commit': row[2],
                'start row': int(row[3]),
                'start col': int(row[4]),
                "code": row[5]
            }
            data_list.append(data)
        
        return data_list

if __name__ == "__main__":
    filename = "atoms2.csv"
    try:
        mapped_data = read_csv(filename)
        for data in mapped_data:
            print(len(mapped_data))
    except Exception as e:
        print(f"An error occurred: {str(e)}")
