#!/usr/bin/env python3
import subprocess, argparse, os.path
from sys import executable, stderr
from glob import glob
from shutil import which

def cli():
    parser = argparse.ArgumentParser(
        description="Apply coccinelle patches onto C files"
    )
    parser.add_argument("-i", "--input", default=["."], help="""
        List of C files to run patches on, separated by spaces. Directories are also accepted.
        If not specified, all *.c files in the current directory, as well as any subdirectories of it,
        will be run.
        """, nargs='*')
    parser.add_argument("-p", "--patch", default=["."], help="""
        List of coccinelle patches to run, separated by spaces. Directories are also accepted.
        If not specified, all *.cocci files in the current directory, as well as any subdirectories of it,
        will be run.
        """, nargs='*')
    parser.add_argument("-o", "--opts", default=[], help="Options to pass to `spatch`",
        nargs=argparse.REMAINDER)
    args = parser.parse_args()

    # check if coccinelle is installed
    if not which('spatch'):
        print("ERROR: coccinelle should be installed before running this tool. Quitting.", file=stderr)
        exit(1)

    # handle files
    f = args.input
    if len(f) == 0:
        f = ["."]

    # handle patches
    patches = []
    if len(args.patch) == 0:
        print("WARNING: No patches supplied via the -p option. Attempting to find patches here...", file=stderr)
        args.patch = ["."]
    for patch in args.patch:
        if os.path.isfile(patch):
            patches.append(patch)
        elif os.path.isdir(patch):
            p = glob(f'{patch}/**/*.cocci', recursive=True)
            if len(p) == 0:
                print(f"WARNING: there is no .cocci files in {patch} or its subdirectories. Skipping.", file=stderr)
            patches.extend(p)
        else:
            print(f"WARNING: {patch} is supplied to the patch argument but is not a valid path. Skipping.", file=stderr)
    if len(patches) == 0:
        print("ERROR: no patches are found. Quitting.", file=stderr)
        exit(1)

    # handle opts
    clear = -1
    for opt in args.opts:
        if opt == "--python":
            print("WARNING: --python option is omitted, as the program will set it for you.", file=stderr)
            clear = args.opts.index(opt)
            break
    if clear > -1:
        args.opts = args.opts[0:clear] + args.opts[clear + 2:]

    # run
    for c in f:
        for patch in patches:
            try:
                run = subprocess.run(
                    ["spatch", "--sp-file", patch, c, "--python", executable] + args.opts,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, universal_newlines=True
                )
                p = run.stdout.strip()
                if len(p) > 0:
                    print(p)
            except subprocess.CalledProcessError as e:
                print(f"STDERR in {patch}: {e.stderr.strip()}", file=stderr)

if __name__ == "__main__":
    cli()