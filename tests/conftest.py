from pathlib import Path

TEST_DATA_PATH = Path(__file__).parent / "data"
INPUTS_DIR = TEST_DATA_PATH / "inputs"
EXPECTED_OUTPUTS_DIR = TEST_DATA_PATH / "expected_outputs"


def pytest_addoption(parser):
    parser.addoption(
        "--overwrite",
        action="store_true",
        default=False,
        help="Enable overwriting of files",
    )
