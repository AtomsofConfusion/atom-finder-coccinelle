from subprocess import run, PIPE, CalledProcessError
from io import StringIO
from sys import stderr

def run_cocci(opts, cocci_patch_path, c_input_path): 
    # keep all paths for this file to avoid additional imports from pathlib

    try:
        result = run(
            ["spatch", "--sp-file", cocci_patch_path, c_input_path] + opts,
            stderr=PIPE, stdout=PIPE, check=True, universal_newlines=True
        )
        output = result.stdout
        data = StringIO(output)
        return data

    except CalledProcessError as e:
        print(f"STDERR in {c_input_path}: {e.stderr.strip()}", file=stderr)