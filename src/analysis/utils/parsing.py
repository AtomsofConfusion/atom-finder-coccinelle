import csv
from pathlib import Path
import re
import pygit2
from clang.cindex import Index, CursorKind, Config
from src.analysis.utils.git import get_file_content_at_commit
from src.run_cocci import run_patches_and_generate_output
from src.analysis.utils.parsing_with_cscope import parse_and_modify_with_cscope
import json 


Config.set_library_file("/home/stavan/miniconda3/envs/atoms/lib/libclang.so")

def is_complex_structure(cursor):
    return cursor.kind in [
        CursorKind.IF_STMT,
        CursorKind.FOR_STMT,
        CursorKind.WHILE_STMT,
        CursorKind.SWITCH_STMT,
        CursorKind.STRUCT_DECL,
    ]


def save_headers_to_temp(
    full_code, output_dir, repo, commit, loaded_headers, invalid_headers
):
    _extract_headers(
        output_dir, full_code, repo, commit, loaded_headers, invalid_headers
    )


def save_all_headers(output_dir, commit, repo):
    # if it's better to save all headers, this can be used
    # doesn't seem to make a difference
    subfolder_tree = commit.tree
    subfolder_tree = repo.get(subfolder_tree["include"].id)
    _save_all_headers(output_dir, subfolder_tree, repo, path_prefix="include")


def _save_all_headers(output_dir, tree, repo, path_prefix):
    for entry in tree:
        entry_path = f"{path_prefix}/{entry.name}".strip("/")
        if entry.type == pygit2.GIT_OBJ_TREE:
            sub_tree = repo.get(entry.id)
            _save_all_headers(output_dir, sub_tree, repo, entry_path)
        elif entry.type == pygit2.GIT_OBJ_BLOB:
            header_name = f"{path_prefix.split('include/')[1]}/{entry.name}"
            path = Path(output_dir / header_name)
            file_content = entry.read_raw().decode()
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text(file_content)


def _extract_headers(output_dir, code, repo, commit, processed, invalid):
    """
    Recursively extract all unique header file names from the C code.

    :param code: C code from which to extract header files.
    :param base_path: The base directory where header files are searched (as a Path object).
    :param processed: A set to keep track of processed header files to avoid cyclic includes.
    :return: A set of all header files included in the code, directly or indirectly.
    """
    header_pattern = re.compile(r"#include\s+<([^>]+)>")
    headers = set(header_pattern.findall(code))
    all_headers = set(headers)

    for header in headers:
        if header in processed[commit] or header in invalid[commit]:
            continue
        if header not in processed[commit]:
            processed[commit].append(header)
            header_name = str(Path("include", header))
            try:
                file_content = get_file_content_at_commit(repo, commit, header_name)
                path = Path(output_dir / header)
                path.parent.mkdir(exist_ok=True, parents=True)
                path.write_text(file_content)
            except Exception as e:
                print(f"Cannot load {header} at {commit} due to {e}")
                invalid[commit].append(header)
                continue
            included_headers = _extract_headers(
                output_dir, file_content, repo, commit, processed, invalid
            )
            all_headers.update(included_headers)
    return all_headers


def parse_file(code, include_dir, file_name):
    index = Index.create()
    tu = index.parse(
        file_name,
        args=["-std=c11", "-nostdinc", f"-I{include_dir}"],
        unsaved_files=[(file_name, code)],
    )
    return tu


def parse_and_modify_functions(code, removed_line_numbers, include_dir, file_name):
    tu = parse_file(code, include_dir, file_name)
    lines = code.splitlines()

    def prepare_modifications(cursor, removed_line_numbers):
        for child in cursor.get_children():
            if child.location.file and file_name not in child.location.file.name:
                continue
            is_function = child.kind == CursorKind.FUNCTION_DECL
            is_complex = is_complex_structure(child)
            continue_inner_search = True
            if is_function or is_complex:
                element_start = child.extent.start.line
                element_end = child.extent.end.line
                element_lines = [line for line in range(element_start, element_end + 1)]

                any_contained = any(
                    line in removed_line_numbers for line in element_lines
                )
                all_contained = all(
                    line in removed_line_numbers for line in element_lines
                )

                # if all contained, the whole function was removed
                if is_function:
                    if not any_contained or all_contained:
                        # Find the compound statement that is the body of the function
                        for c in child.get_children():
                            if c.kind == CursorKind.COMPOUND_STMT:
                                # Calculate the start and end offsets for the body
                                body_start_line = c.extent.start.line
                                body_end_line = c.extent.end.line - 2
                                # Store the offsets and the count of newlines to preserve formatting
                                lines[body_start_line : body_end_line + 1] = [
                                    ""
                                    for _ in range(body_end_line - body_start_line + 1)
                                ]
                                break

                if all_contained and len(element_lines) > 2:
                    for line in element_lines:
                        removed_line_numbers.remove(line)

                if all_contained or not any_contained:
                    continue_inner_search = False

            if continue_inner_search:
                prepare_modifications(child, removed_line_numbers)

    modified_line_numbers = list(set(removed_line_numbers))
    prepare_modifications(tu.cursor, modified_line_numbers)
    return "\n".join(lines), modified_line_numbers


def _normalize_code(text):
    """
    Normalize code by removing extra spaces around punctuation and making it lowercase.
    This function also standardizes common variations in array declarations.
    """
    # text = text.replace('\t', ' ').replace('\n', ' ')
    # text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with one
    # text = re.sub(r'\s*\[\s*', '[', text)  # Remove spaces around [
    # text = re.sub(r'\s*\]\s*', ']', text)  # Remove spaces around ]
    # text = re.sub(r'\s*\(\s*', '(', text)  # remove spaces around parentheses
    # text = re.sub(r'\s*\)\s*', ')', text)  # remove spaces around parentheses
    # text = re.sub(r'\s*\)\s*', '*', text)  # remove spaces around *
    return text.replace(" ", "")


def contains_expression(node, expression, line_number=None):
    """
    Check if the normalized node text contains the normalized expression.
    """
    if line_number:
        if line_number < node.extent.start.line or line_number > node.extent.end.line:
            return False
    node_text = " ".join([token.spelling for token in node.get_tokens()])
    if expression.endswith(";"):
        expression = expression[:-1]
    normalized_node_text = _normalize_code(node_text)
    normalized_expression = _normalize_code(expression)
    return normalized_expression in normalized_node_text


def find_smallest_containing_node(
    node, expression, line_number, ancestors, best_match=None
):
    """
    Recursively find the smallest node that contains the given expression.
    """
    expression = expression.strip()
    if contains_expression(node, expression, line_number):
        ancestors.append(node)
        best_match = node
        # print("--------------------")
        # node_text = " ".join([token.spelling for token in node.get_tokens()])
        # print(node_text)
        # print("**************************88")
        children = [child for child in node.get_children()]
        for child in children:
            # node_text = " ".join([token.spelling for token in child.get_tokens()])
            # print(node_text)
            # print("***************8")
            inner_best_match = find_smallest_containing_node(
                child, expression, line_number, ancestors, best_match
            )
            if inner_best_match is not None:
                best_match = inner_best_match
                break
    return best_match


def get_code_from_extent(code, extent):
    lines = code.splitlines()
    start = extent.start
    end = extent.end

    if start.line == end.line:
        return lines[start.line - 1][start.column - 1 : end.column - 1]

    code_lines = []
    code_lines.append(lines[start.line - 1][start.column - 1 :])
    for line in range(start.line, end.line - 1):
        code_lines.append(lines[line])
    try:
        code_lines.append(lines[end.line - 1][: end.column - 1])
    except:
        pass
    return code_lines


def get_function_or_statement_context(root_node, full_code, source_code, line_number):

    # _run_diagnostics(tu, file_path)

    ancestors = []
    try:
        node = find_smallest_containing_node(
            root_node, source_code, line_number, ancestors
        )
    except UnicodeDecodeError as e:
        print(f"Could not parse file")
        return None, None

    # if node is not None:
    #     ancestors.reverse()
    #     # Ensure we capture broader context by moving up the AST if needed
    #     for parent_node in ancestors:
    #         if parent_node.kind in (clang.cindex.CursorKind.FUNCTION_DECL,
    #                                    clang.cindex.CursorKind.CXX_METHOD,
    #                                    clang.cindex.CursorKind.STRUCT_DECL,
    #                                    clang.cindex.CursorKind.CLASS_DECL):
    #             node = parent_node
    #             break
    if node is not None and node != root_node:
        return node, get_code_from_extent(full_code, node.extent)
    return None, None


def run_coccinelle_for_file_at_commit(
    repo,
    file_name,
    commit,
    modified_line_numbers,
    temp_dir,
    loaded_headers,
    invalid_headers,
    patches_to_skip=None,
    save_headers=True,
):
    atoms = []
    headers_dir = Path(temp_dir, "headers")
    content = get_file_content_at_commit(repo, commit, file_name)
    if save_headers:
        save_headers_to_temp(
            commit=commit,
            output_dir=headers_dir,
            repo=repo,
            full_code=content,
            loaded_headers=loaded_headers,
            invalid_headers=invalid_headers,
        )
    shorter_content, modified_lines = parse_and_modify_with_cscope(
        content, modified_line_numbers, temp_dir, file_name
    )
    # shorter_content, modified_lines = parse_and_modify_functions(
    #     content, modified_line_numbers, headers_dir, file_name
    # )
    # # DEBUG: Save content and modified lines to permanent Debug directory
    # debug_dir = Path("Debug_cscope")
    # debug_dir.mkdir(parents=True, exist_ok=True)

    # # Save shorter_content
    # debug_content_path = debug_dir / f"{file_name}.shorter"
    # debug_content_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure all parent directories exist
    # debug_content_path.write_text(shorter_content)


    # # Save modified_line_numbers as JSON for easier inspection
    # debug_lines_path = debug_dir / f"{file_name}.modified_lines.json"
    # debug_lines_path.parent.mkdir(parents=True, exist_ok=True)
    # debug_lines_path.write_text(json.dumps(modified_line_numbers, indent=2))


    # Define file paths within the temporary directory
    input = Path(temp_dir, "input", file_name)
    input.parent.mkdir(parents=True, exist_ok=True)
    input.write_text(shorter_content)

    output = Path(temp_dir, "output.csv")
    input_dir = Path(temp_dir, "input")
    # now, run coccinelle patches

    # task = partial(find_atoms, input_dir, output, None, PATCHES_TO_SKIP)
    run_patches_and_generate_output(
        input_dir, output, temp_dir, False, None, patches_to_skip, False
    )

    with open(output, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 1:
                continue
            atom, path, start_line, start_col, end_line, end_col, code = row
            file_name = path.split(f"{input_dir}/")[1]
            if int(start_line) in modified_lines:
                row[1] = file_name
                atoms.append(row)

    return atoms
