#!/usr/bin/env python3
import os
import re
import uuid
import shutil
import subprocess
from clang.cindex import Index, CursorKind

# ------------------------------------------------------------------
# Helper: preprocess content _in memory_, write only the output file
# ------------------------------------------------------------------
import os, re

def preprocess_in_memory(content, output_dir, base_name):
    """
    - content: the raw source as one string
    - output_dir: where to drop preprocessed_<base_name>
    Returns:
      - out_path: full path to the preprocessed file
      - original_pp: dict[line_no, original_pp_line]
      - out_lines: List[str] of the preprocessed file (with newlines)
    """
    os.makedirs(output_dir, exist_ok=True)
    pp_pat     = re.compile(r'^\s*#\s*(ifdef|else|endif|ifndef|if|elif)')
    inc_pat    = re.compile(r'^\s*#\s*include')
    define_pat = re.compile(r'^\s*#\s*define')

    # Split into lines, preserving newline chars
    lines = content.splitlines(keepends=True)
    original_pp = {}
    out_lines   = []
    i = 0

    while i < len(lines):
        line = lines[i]
        ln = i + 1

        # 1) Preprocessor directives → comment out, but keep one‑to‑one
        if pp_pat.match(line):
            original_pp[ln] = line.rstrip("\n")
            out_lines.append("// " + line)
            i += 1

        # 2) #include → keep & record
        elif inc_pat.match(line):
            original_pp[ln] = line.rstrip("\n")
            out_lines.append(line)
            i += 1

        # 3) #define (possibly multi‑line) → record & emit each line
        elif define_pat.match(line):
            buf = [line.rstrip("\n")]
            j = i + 1
            # collect continuation lines ending with '\'
            while buf[-1].endswith("\\") and j < len(lines):
                buf.append(lines[j].rstrip("\n"))
                j += 1

            # record and emit **one** output line **per** original line
            for k, txt in enumerate(buf):
                original_pp[ln + k] = txt
                out_lines.append(txt + "\n")

            i = j

        # 4) Regular code → pass through
        else:
            out_lines.append(line)
            i += 1

    # Write the preprocessed file
    out_path = os.path.join(output_dir, f"preprocessed_{base_name}")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.writelines(out_lines)

    return out_path, original_pp, out_lines


# ------------------------------------------------------------------
# cscope & clang helpers
# ------------------------------------------------------------------
def extract_symbol_from_line(line):
    reserved = {
      "auto","break","case","char","const","continue","default","do",
      "double","else","enum","extern","float","for","goto","if","int",
      "long","register","return","short","signed","sizeof","static",
      "struct","switch","typedef","union","unsigned","void",
      "volatile","while"
    }
    for tok in re.findall(r"\b([A-Za-z_]\w*)\b", line):
        if tok not in reserved:
            return tok
    return None

def build_cscope_db(temp_dir, file_path):
    db = os.path.join(temp_dir, f"cscope_db_{uuid.uuid4().hex}")
    os.makedirs(db, exist_ok=True)
    with open(os.path.join(db, "cscope.files"), "w") as f:
        f.write(file_path + "\n")
    subprocess.run(
        ["cscope", "-b", "-q", "-k", "-i", "cscope.files"],
        cwd=db, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
    )
    return db

def search_cscope(db, opt, pat):
    res = subprocess.run(
        ["cscope", "-dL", opt, pat],
        cwd=db, capture_output=True, text=True
    )
    lines = res.stdout.strip().splitlines()
    return lines if lines and lines != [""] else []

def get_function_for_line(db, ln, src_line):
    sym = extract_symbol_from_line(src_line)
    if not sym:
        return None

    results = search_cscope(db, "-0", sym)
    
    for entry in results:
        parts = entry.split()
        if len(parts) >= 3 and parts[2].isdigit() and int(parts[2]) == ln:
            return parts[1]
    return None

def get_function_definition_line(db, fname, func):
    for entry in search_cscope(db, "-1", func):
        parts = entry.split()
        if len(parts) >= 3 and os.path.basename(parts[0]) == os.path.basename(fname):
            if parts[2].isdigit():
                return int(parts[2])
    return None

def extract_preserved_function(lines, db, func, start_ln):
    """
    Extract lines[start_ln-1 : boundary), where 'boundary' is the first
    NON-blank/non-brace line whose function != func.
    """

    n = len(lines)
    # 1) Precompute stripped versions
    stripped = [line.strip() for line in lines]

    # 2) Build list of candidate indices (0-based) to check via get_function_for_line
    candidates = [
        i for i in range(start_ln - 1, n)
        if stripped[i] and stripped[i] not in {"{", "}"}
    ]

    # 3) Binary search over candidates to find the first 'other' function
    lo, hi = 0, len(candidates)
    while lo < hi:
        mid = (lo + hi) // 2
        idx = candidates[mid]
        other = get_function_for_line(db, idx + 1, lines[idx])

        if other is not None and other != func:
            # we’ve found a boundary at or before mid
            hi = mid
        else:
            # still inside this function; keep searching to the right
            lo = mid + 1

    # 4) Determine the slice boundary in the original 'lines'
    if lo < len(candidates):
        boundary = candidates[lo]
    else:
        boundary = n   # no break found → take everything

    # 5) Slice out everything from start to boundary (including blanks/braces)
    return lines[start_ln - 1 : boundary]


def get_global_definitions_by_lines(path, lines=None):
    """
    If `lines` is provided, it must be the same list that was written to `path`.
    Otherwise we read & split the file once.
    """
    if lines is None:
        with open(path, "r") as f:
            src = f.read().splitlines(keepends=True)
    else:
        src = lines
    out = [""] * len(src)

    idx = Index.create()
    # You can adjust -I flags here if you have more include dirs
    tu  = idx.parse(path, args=["-std=c11", "-nostdinc"])

    def visit(node):
        loc = node.location
        if not loc.file or loc.file.name != path:
            return
        if node.kind in {
            CursorKind.VAR_DECL,
            CursorKind.STRUCT_DECL,
            CursorKind.ENUM_DECL,
            CursorKind.MACRO_DEFINITION
        } and node.semantic_parent.kind == CursorKind.TRANSLATION_UNIT:
            s, e = node.extent.start.line, node.extent.end.line
            for j in range(s-1, e):
                out[j] = src[j].rstrip("\n")

    for child in tu.cursor.get_children():
        visit(child)

    return out



def parse_and_modify_with_cscope(content,
                                 modified_line_numbers,
                                 temp_dir,
                                 file_name):
    """
    - content: full source text
    - modified_line_numbers: list[int]
    - temp_dir: writes ONLY preprocessed_<file_name> + cscope DB
    - file_name: e.g. "foo.c"
    """
    os.makedirs(temp_dir, exist_ok=True)

    # 1) Preprocess _in memory_
    preproc_path, pp_lines, preproc_lines = preprocess_in_memory(content, temp_dir, file_name)
    assert len(preproc_lines) == len(content.splitlines(keepends=True)), \
    f"Line count mismatch: {len(preproc_lines)} vs {len(content.splitlines(True))}"


    # 2) Use the in‑memory lines for everything except cscope:
    all_lines = preproc_lines

    # 3) Build cscope DB
    cs_db = build_cscope_db(temp_dir, preproc_path)
    # 4) Extract global definitions
    
    globals_buf = get_global_definitions_by_lines(preproc_path, lines=all_lines)
    for ln, txt in pp_lines.items():
        globals_buf[ln-1] = txt

    # 5) Identify affected functions
    funcs = set()
    for ln in modified_line_numbers:
        if 1 <= ln <= len(all_lines):
            fn = get_function_for_line(cs_db, ln, all_lines[ln-1])
            if fn:
                funcs.add(fn)

    # 6) Splice in modified functions
    for func in funcs:
        start_ln = get_function_definition_line(cs_db, file_name, func)

        if not start_ln:
            continue

        body = extract_preserved_function(all_lines, cs_db, func, start_ln)
        
        for off, line in enumerate(body):
            pos = start_ln - 1 + off
            if pos < len(globals_buf):
                globals_buf[pos] = line.rstrip("\n")

    # 7) Cleanup
    shutil.rmtree(cs_db, ignore_errors=True)

    # 8) Return final content and print timings
    shorter = "".join((L if L.endswith("\n") else L + "\n") for L in globals_buf)

    return shorter, sorted(modified_line_numbers)
