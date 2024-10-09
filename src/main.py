# OMIT !/usr/bin/env python3
import os.path
from subprocess import run, PIPE, CalledProcessError
from argparse import ArgumentParser, REMAINDER
from sys import executable, stderr, exit
from glob import iglob
from shutil import which

def cli():
    parser = ArgumentParser(
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
        nargs=REMAINDER)
    args = parser.parse_args()

    # check if coccinelle is installed
    if not which('spatch'):
        print("ERROR: coccinelle should be installed before running this tool. Quitting.", file=stderr)
        exit(1)


    # handle files
    # f = args.input
    # if len(f) == 0:
    #     print("WARNING: No files supplied via the -i option. Attempting to find files here...", file=stderr)
    #     f = ["."]

    # # handle opts
    # clear = -1
    # for opt in args.opts:
    #     if opt == "--python":
    #         print("WARNING: --python option is omitted, as the program will set it for you.", file=stderr)
    #         clear = args.opts.index(opt)
    #         break
    # if clear > -1:
    #     args.opts = args.opts[0:clear] + args.opts[clear + 2:]

    # # handle patches
    # if len(args.patch) == 0:
    #     print("WARNING: No patches supplied via the -p option. Attempting to find patches here...", file=stderr)
    #     args.patch = ["."]
    # for patch in args.patch:
    #     if os.path.isfile(patch):
    #         apply(patch, args.opts, f)
    #     elif os.path.isdir(patch):
    #         hasFiles = False
    #         for p in iglob(f'{patch}/**/*.cocci', recursive=True):
    #             hasFiles = True
    #             apply(p, args.opts, f)
    #         if not hasFiles:
    #             print(f"WARNING: there is no .cocci files in {patch} or its subdirectories. Skipping.", file=stderr)
    #     else:
    #         print(f"WARNING: {patch} is supplied to the patch argument but is not a valid path. Skipping.", file=stderr)

    try:
        # OS specifc?
        result = run(['bash', 'script.sh'], check=True)
    except CalledProcessError as e:
        print(f"An error occurred while executing setup.sh: {e}")
        exit(1)

# def apply(patch, opts, f):
#     for c in f:
#         try:
#             r = run(
#                 ["spatch", "--sp-file", patch, c, "--python", executable] + opts,
#                 stdout=PIPE, stderr=PIPE, check=True, universal_newlines=True
#             )
#             p = r.stdout.strip()
#             if len(p) > 0:
#                 print(p)
#         except CalledProcessError as e:
#             print(f"STDERR in {patch}: {e.stderr.strip()}", file=stderr)

if __name__ == "__main__":
    cli()