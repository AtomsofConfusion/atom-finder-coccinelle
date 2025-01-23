import shutil
from pathlib import Path
from pytest import fixture
from src.exceptions import SPatchVersionError
from src.utils import check_cocci_version

TEST_DATA_PATH = Path(__file__).parent / "data"
INPUTS_DIR = TEST_DATA_PATH / "inputs"
EXPECTED_OUTPUTS_DIR = TEST_DATA_PATH / "expected_outputs"


def pytest_addoption(parser):
    parser.addoption(
        "--overwrite",
        action="store_true",
        default=False,
        help="Regenerate expected outputs",
    )
    parser.addoption(
        "--test",
        action="store",
        default=None,
        help="Specify patch to run",
    )


@fixture(scope="session", autouse=True)
def check_spatch_version():
    try:
        check_cocci_version()
    except SPatchVersionError as e:
        pytest.fail(str(e))
      

@fixture(scope="module")
def output_dir():
    output_dir_path = TEST_DATA_PATH / "output"
    output_dir_path.mkdir(exist_ok=True)
    yield output_dir_path
    shutil.rmtree(output_dir_path)

