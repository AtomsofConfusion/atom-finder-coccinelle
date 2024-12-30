import click
from pathlib import Path
from io import StringIO

from src.option_select import select
from src.run_cocci import run_cocci, COCCI_DIR, find_atoms, CocciPatch, run_patches_and_generate_output
from src.utils import append_to_csv
from src.log import logging

def list_patches():
    """List all available patches."""
    return [patch.name.lower() for patch in CocciPatch]


@click.command
@click.argument("input-path", type=Path)
@click.option("-o", "--output-dir", type=Path, default=".")
# @click.option(
#     '--scope',
#     type=click.Choice(['all', 'select']),
#     prompt='Choose an option to compare all or just a single file'
# )


@click.option(
    "--patch",
    type=click.Choice(list_patches(), case_sensitive=False),
    prompt=False,
    help="Select a patch to apply",
)
@click.option(
    "-v", "--verbosity", type=str, default=0, required=False, help="Enter 0 or 1"
)
def atom_finder(input_path, output_dir, patch, verbosity):
    cocci_patch = CocciPatch.from_string(patch) if patch else None
    if not input_path.exists():
        logging.error(f"{input_path} does not exist")
        return

    if not output_dir.is_dir():
        output_dir.mkdir(parents=True)

    run_patches_and_generate_output(input_path, output_dir, cocci_patch)

    # if(scope=='select'):
    #     patch_list = [select(patch_list)]

    # input_list = []
    # pattern = ['*.c','*.cpp']
    # for extension in pattern:
    #     input_list.extend(file for file in input.glob(extension))

    # data = StringIO()
    # for input in input_list:
    #     for patch in patch_list:
    #         data.write(run_cocci([], (Path.cwd() / "cocci" / patch), input).getvalue())

    # with open('output.csv', 'w', newline='') as csv_file:
    #     csv_file.write(data.getvalue())


if __name__ == "__main__":
    atom_finder()
