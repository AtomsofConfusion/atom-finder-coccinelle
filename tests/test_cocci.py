import pytest
import csv
import os
from pathlib import Path
from src.run_cocci import CocciPatch, run_patches_and_generate_output
from tests.conftest import INPUTS_DIR, EXPECTED_OUTPUTS_DIR
from tests.test_utils import compare
from src.utils import append_to_csv, write_to_csv, parse_csv_data


@pytest.mark.parametrize("patch", [patch for patch in CocciPatch])
def test_cocci_patches(patch, pytestconfig, output_dir):
    patch_to_test = pytestconfig.getoption("test")
    if patch_to_test is not None and patch_to_test.lower() != patch.name.lower():
        pytest.skip(f"Skipping")

    input_file = INPUTS_DIR / f"{patch.name.lower()}.c"
    if not input_file.is_file():
        pytest.skip(f"Missing input {input_file}")
    expected_output_file = EXPECTED_OUTPUTS_DIR / f"{patch.name.lower()}.csv"

    overwrite = pytestconfig.getoption("overwrite")

    if not overwrite and not expected_output_file.is_file():
        pytest.skip(f"Missing expected file {expected_output_file}")

    run_patches_and_generate_output(input_file, output_dir, patch)
    output_file_path = output_dir / f"{patch.value.stem}.csv"
    assert output_file_path.is_file()
    actual = output_file_path.read_text()
    assert actual

    if overwrite:
        write_to_csv(expected_output_file, actual.split("\n"))
    else:
        actual_rows = parse_csv_data(actual)
        with open(expected_output_file, newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            expected_rows = list(csv_reader)

        compare(actual_rows, expected_rows)
