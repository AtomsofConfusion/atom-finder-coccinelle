from pathlib import Path
import tempfile

from tqdm import tqdm

from src import COCCI_DIR, ROOT_DIR
from src.analysis.utils.utils import copy_from_csv
from src.run_cocci import run_patches_and_generate_output
from src.log import logger


OUTPUT_PATH = Path("../results/latest/atoms.csv")
LAST_PROCESSED_PATH = Path("../last_processed/latest/last_processed.json")
REPO_PATH = (ROOT_DIR.parent / "atoms/projects/linux").absolute()  # Path to the Linux kernel Git repository

# TODO /home/ubuntu/atoms/projects/linux/lib/test_bpf.c this file to see why there are duplicates

def process_with_continuation(directory: Path, output: Path):

    cocci_dir = COCCI_DIR / "bugfix"
    last_processed = None
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LAST_PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    if LAST_PROCESSED_PATH.exists():
        with LAST_PROCESSED_PATH.open('r') as file:
            last_processed = file.read().strip()


   # Determine the starting index if continuation is needed
    c_files = list(directory.rglob('*.c'))
    start_index = 0
    if last_processed:
        for i, c_file in enumerate(c_files):
            if c_file.name == last_processed:
                start_index = i + 1
                break


    with tempfile.TemporaryDirectory() as temp_dir:
       temp_output = Path(temp_dir, "output.csv")
       with tqdm(total=len(c_files), initial=start_index, desc='Processing C files') as pbar:
            for c_file in c_files[start_index:]:
                try:
            
                    temp_output.open("w").close()
                    logger.debug(f"Current file {c_file}")
                    run_patches_and_generate_output(input_path=c_file, 
                                                    output_path=temp_output, 
                                                    temp_dir=Path(temp_dir), 
                                                    cocci_dir=cocci_dir,
                                                    split_output=False)
                    

                    # Write the name of the last processed file to the state file
                    with LAST_PROCESSED_PATH.open('w') as file:
                        file.write(c_file.name)
                    copy_from_csv(temp_output, output)

                    # Update the progress bar after each file is processed
                except Exception as e:
                    print(f"An error occurred while processing {c_file}")
                    print(e)
                pbar.update(1)

# Example usage
if __name__ == "__main__":
    process_with_continuation(REPO_PATH, OUTPUT_PATH)
