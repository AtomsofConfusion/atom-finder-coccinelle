#!/usr/bin/env python3
import subprocess, argparse, os.path
from sys import executable, stderr
from glob import glob

def cli():
    parser = argparse.ArgumentParser(
        description="Apply coccinelle patches onto C files"
    )
    parser.add_argument("file", help="C file to run patches on")
    parser.add_argument("-p", "--patch", default=[], help="""
        List of coccinelle patches to run, separated by spaces. If not specified, all *.cocci files
        in the current directory will be run.
        """, nargs='*')
    parser.add_argument("-o", "--opts", default=[], help="Options to pass to `spatch`",
        nargs=argparse.REMAINDER)
    args = parser.parse_args()

    # handle patches
    patches = args.patch
    if len(patches) == 0:
        print("WARNING: No patches supplied via the -p option. Attempting to find patches here...", file=stderr)
        patches = glob("*.cocci")
    if len(patches) == 0:
        print("ERROR: No patches found in the current directory.", file=stderr)
        exit(1)

    # handle file
    if not os.path.isfile(args.file):
        print(f"ERROR: {args.file} does not exist. Quitting.")
        exit(1)

    # handle opts
    clear = -1
    for opt in args.opts:
        if opt == "--python":
            print("WARNING: --python option is omitted, as the program will set it for you.")
            clear = args.opts.index(opt)
            break
    if clear > -1:
        args.opts = args.opts[0:clear] + args.opts[clear + 2:]

    # run
    for patch in patches:
        if not os.path.isfile(patch):
            print(f"ERROR: patch {patch} does not exist. Skipping.")
            continue
        try:
            run = subprocess.run(
                ["spatch", "--sp-file", patch, args.file, "--python", executable] + args.opts,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, universal_newlines=True
            )
            p = run.stdout.strip()
            if len(p) > 0:
                print(p)
        except subprocess.CalledProcessError as e:
            print(f"STDERR in {patch}: {e.stderr.strip()}", file=stderr)