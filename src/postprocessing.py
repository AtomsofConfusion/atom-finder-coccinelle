import csv



def read_csv_generator(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            yield row


def postprocess(file_path, output_file_path):
    seen = set() 
    filtered_data = [] 

    with open(output_file_path, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in read_csv_generator(file_path):
            key = tuple(row[1:-1])
            if key not in seen:
                seen.add(key)
                filtered_data.append(row)

                if len(filtered_data) > 10000: 
                    filtered_data = remove_contained_code(filtered_data)
                    writer.writerows(filtered_data)
                    filtered_data.clear()

        # Final processing for any remaining data
        if filtered_data:
            filtered_data = remove_contained_code(filtered_data)
            writer.writerows(filtered_data)


