#!/usr/bin/env python3
import subprocess, argparse, os.path
from sys import executable, stderr
from glob import glob
from shutil import which

def cli():
    parser = argparse.ArgumentParser(
        description="Apply coccinelle patches onto C files"
    )
    parser.add_argument("-f", "--file", default=[], help="""
        List of C files to run patches on, separated by spaces. If not specified, all *.c files
        in the current directory will be run.
        """, nargs='*')
    parser.add_argument("-p", "--patch", default=[], help="""
        List of coccinelle patches to run, separated by spaces. If not specified, all *.cocci files
        in the current directory will be run.
        """, nargs='*')
    parser.add_argument("-o", "--opts", default=[], help="Options to pass to `spatch`",
        nargs=argparse.REMAINDER)
    args = parser.parse_args()

    # check if coccinelle is installed
    if not which('spatch'):
        print("ERROR: coccinelle should be installed before running this tool. Quitting.", file=stderr)
        exit(1)

    # handle files
    f = args.file
    if len(f) == 0:
        print("WARNING: No C files supplied via the -f option. Attempting to find C files here...", file=stderr)
        f = glob("*.c")
    if len(f) == 0:
        print("ERROR: No C files found in the current directory. Quitting.", file=stderr)
        exit(1)

    # handle patches
    patches = args.patch
    if len(patches) == 0:
        print("WARNING: No patches supplied via the -p option. Attempting to find patches here...", file=stderr)
        patches = glob("*.cocci")
    if len(patches) == 0:
        print("ERROR: No patches found in the current directory. Quitting.", file=stderr)
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
        if not os.path.isfile(c):
            print(f"WARNING: file {c} does not exist. Skipping.", file=stderr)
            continue
        for patch in patches:
            if not os.path.isfile(patch):
                print(f"WARNING: patch {patch} does not exist. Skipping.", file=stderr)
                continue
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