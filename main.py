#!/usr/bin/env python3
import subprocess, argparse
from sys import executable
from glob import glob

parser = argparse.ArgumentParser(
    description="Apply coccinelle patches onto C files"
)
parser.add_argument("file", help="C file to run patches on")
parser.add_argument("-p", "--patch", default=[], help="""
    List of coccinelle patches to run, separated by spaces. If not specified, all *.cocci files
    in the current directory will be run.
    """, nargs='*')
parser.add_argument("-o", "--opts", default=[], help="Options to pass to `spatch`", nargs='*')
args = parser.parse_args()

patches = args.patch if len(args.patch) > 0 else glob("*.cocci")


# run
for patch in patches:
    try:
        run = subprocess.run(
            ["spatch", "--sp-file", patch, args.file, "--python", sys.executable],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, universal_newlines=True
        )
        p = run.stdout.strip()
        if len(p) > 0:
            print(p)
    except subprocess.CalledProcessError as e:
        print(e.stderr.strip())