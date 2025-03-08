from pathlib import Path
import tempfile

from src import COCCI_DIR, ROOT_DIR
from src.run_cocci import run_patches_and_generate_output
from src.log import logger


OUTPUT_PATH = Path("../results/latest/atoms.json")
LAST_PROCESSED_PATH = Path("../last_processed/latest/last_processed.json")
REPO_PATH = (ROOT_DIR.parent / "atoms/projects/linux").absolute()  # Path to the Linux kernel Git repository

def process_with_continuation(directory: Path):

    cocci_dir = COCCI_DIR / "bugfix"
    last_processed = None
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LAST_PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    if LAST_PROCESSED_PATH.exists():
        with LAST_PROCESSED_PATH.open('r') as file:
            last_processed = file.read().strip()

    c_files = list(directory.rglob('*.c'))
    start_processing = not last_processed

    with tempfile.TemporaryDirectory() as temp_dir:
        output = Path(temp_dir, "output.csv")
        for c_file in c_files:
            output.open("w").close()
            if not start_processing:
                if c_file.name == last_processed:
                    start_processing = True
                continue
            
            logger.info(f"Current file {c_file}")
            run_patches_and_generate_output(input_path=c_file, 
                                            output_path=OUTPUT_PATH, 
                                            temp_dir=Path(temp_dir), 
                                            cocci_dir=cocci_dir,
                                            split_output=False)
            

            # Write the name of the last processed file to the state file
            with LAST_PROCESSED_PATH.open('w') as file:
                file.write(c_file.name)

# Example usage
if __name__ == "__main__":
    process_with_continuation(REPO_PATH)
