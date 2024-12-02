# OMIT !/usr/bin/env python3
from pathlib import Path
import click
from io import StringIO

from src.option_select import select
from src.run_cocci import run_cocci

@click.command
@click.option(
    "-i",
    "--input",
    type=Path,
    required=True,
    help="Directory containing your C source files.",
)
@click.option(
    '--scope',
    type=click.Choice(['all', 'select']), 
    prompt='Choose an option to compare all or just a single file'
)
@click.option(
    "-v",
    "--verbosity", 
    type=str,
    default=0,
    required=False,
    help = "Enter 0 or 1"
)
def cli(input, scope, verbosity):
    if not input.is_dir():
        raise Exception(f"input path is not valid")

    patch_list = (Path.cwd() / "cocci").glob("*.cocci")
    patch_list = list(map(lambda file: file.name, patch_list))

    if(scope=='select'):
        patch_list = [select(patch_list)]

    input_list = []
    pattern = ['*.c','*.cpp']
    for extension in pattern:
        input_list.extend(file for file in input.glob(extension))

    data = StringIO()
    for input in input_list:
        for patch in patch_list:
            data.write(run_cocci([], (Path.cwd() / "cocci" / patch), input).getvalue())

    with open('output.csv', 'w', newline='') as csv_file: 
        csv_file.write(data.getvalue())
    


if __name__ == "__main__":
    cli()