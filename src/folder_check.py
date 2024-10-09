from pathlib import Path
import warnings

def check_all():

    folder_lists = ["cocci_outputs", "cocci", "tests/data/expected_outputs", "tests/data/inputs"]

    for item in folder_lists:
        path = Path(item)
        
        if not path.is_dir():
            raise OSError(f"The {item} folder does not exist. The project structure may have been modified.")

        # if not any(path.iterdir()):
        #     if item!=list[0]:
        #         raise OSError(f"The {item} folder is empty. Run the tool first to generate outputs.")
    
    print(f"All four directories exist and are not empty.")

# def preprocess():
    
#     df = pd.read_csv('your_file.csv', header=None)

#     df_sorted = df.sort_values(by=df.columns[2])

#     df_sorted.to_csv('sorted_file.csv', index=False)