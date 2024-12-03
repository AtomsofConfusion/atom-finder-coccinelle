import pytest
import csv
from pathlib import Path
from src.run_cocci import run_cocci, CocciPatch
from tests.conftest import INPUTS_DIR, EXPECTED_OUTPUTS_DIR
from tests.test_utils import compare
from src.utils import append_to_csv, write_to_csv, parse_csv_data


@pytest.mark.parametrize("patch", [patch for patch in CocciPatch])
def test_cocci_patches(patch, pytestconfig):
        
    input_file = INPUTS_DIR / f"{patch.name.lower()}.c"
    if not input_file.is_file():
        pytest.skip(f"Missing input {input_file}")
    expected_output_file = EXPECTED_OUTPUTS_DIR / f"{patch.name.lower()}.csv"

    overwrite = pytestconfig.getoption("overwrite")

    if not overwrite and not expected_output_file.is_file():
        pytest.skip(f"Missing expected file {expected_output_file}")
    actual = run_cocci(patch.value, input_file, ["--quiet"])
    assert actual

    if overwrite:
        write_to_csv(expected_output_file, actual.split("\n"))
    else:
        actual_rows = parse_csv_data(actual)
        with open(expected_output_file, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            expected_rows = list(csv_reader)
    
        compare(actual_rows, expected_rows)
