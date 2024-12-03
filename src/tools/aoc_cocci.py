import click
from pathlib import Path
from io import StringIO

from src.option_select import select
from src.run_cocci import run_cocci, COCCI_DIR, find_atoms, CocciPatch
from src.utils import append_to_csv


def list_patches():
    """List all available patches."""
    return [patch.name.lower() for patch in CocciPatch]


@click.command
@click.argument("input", type=Path)
@click.option("-o", "--output", type=Path, default=None)
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
def atom_finder(input, output, patch, verbosity):
    cocci_patch = CocciPatch.from_string(patch) if patch else None
    atoms_per_patches = find_atoms(input_path=input, output=output, patch=cocci_patch)

    if not input.is_dir():
        raise Exception(f"input path is not valid")

    if output is None:
        output = Path("output.csv")

    if output.is_file():
        output.unlink()

    if not output.parent.is_dir():
        output.parent.mkdir(parents=True)

    # TODO support very large outputs
    # this should be optimized
    # consider writing to separate files
    for _, atoms in atoms_per_patches.items():
        append_to_csv(output, atoms.split("\n"))

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
