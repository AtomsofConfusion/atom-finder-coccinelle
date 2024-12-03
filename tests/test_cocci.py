import pytest
import csv
from pathlib import Path
from src.run_cocci import run_cocci, CocciPatch
from tests.conftest import INPUTS_DIR, EXPECTED_OUTPUTS_DIR
from tests.test_utils import compare


@pytest.mark.parametrize("patch", [patch for patch in CocciPatch])
def test_cocci_patches(patch):
    input_file = INPUTS_DIR / f"{patch.name.lower()}.c"
    if not input_file.is_file():
        pytest.skip(f"Missing input {input_file}")
    expected_output_file = EXPECTED_OUTPUTS_DIR / f"{patch.name.lower()}.csv"
    if not expected_output_file.is_file():
        pytest.skip(f"Missing expected file {expected_output_file}")
    actual = run_cocci(patch.value, input_file, ["--quiet"])
    assert actual
    actual_rows = [row.split(",") for row in actual.split("\n")]
    list_of_rows = None
    with open(expected_output_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        expected_rows = list(csv_reader)
   
    compare(actual_rows, expected_rows)

    