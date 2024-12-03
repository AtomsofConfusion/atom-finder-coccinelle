import pytest
import csv
import os
from pathlib import Path
from src.run_cocci import run_cocci, CocciPatch
from tests.conftest import INPUTS_DIR, EXPECTED_OUTPUTS_DIR
from tests.test_utils import compare
from src.utils import append_to_csv, write_to_csv, parse_csv_data


def is_running_on_ci():
    ci_env_vars = [
        'CI',
        'GITHUB_ACTIONS',
    ]

    # Check if any known CI environment variable is set
    for var in ci_env_vars:
        if os.getenv(var):
            return True

    return False


# TODO these are failing on CI
# first of all, install Coccinelle from source and then debug
skip_on_ci = [CocciPatch.ASSIGNMENT_AS_VALUE, CocciPatch.IMPLICIT_PREDICATE, CocciPatch.OMITTED_CURLY_BRACES, CocciPatch.TYPE_CONVERSION]


@pytest.mark.parametrize("patch", [patch for patch in CocciPatch])
def test_cocci_patches(patch, pytestconfig):
    if is_running_on_ci():
        if patch in skip_on_ci:
            pytest.skip(f"Skipping on CI")

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
        with open(expected_output_file, newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            expected_rows = list(csv_reader)

        compare(actual_rows, expected_rows)
