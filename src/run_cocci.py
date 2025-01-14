import csv
import shutil
import subprocess
import tempfile
from enum import Enum
from pathlib import Path
from typing import Optional, Dict
from io import StringIO
from sys import stderr

from src import COCCI_DIR
from src.log import logging
from src.exceptions import RunCoccinelleError
from src.utils import run, check_cocci_version


class CocciPatch(Enum):
    ASSIGNMENT_AS_VALUE = Path(COCCI_DIR / "assignment_as_value.cocci")
    CHANGE_OF_LITERAL_ENCODING = Path(COCCI_DIR / "change_of_literal_encoding.cocci")
    COMMA_OPERATOR = Path(COCCI_DIR / "comma_operator.cocci")
    CONDITIONAL_OPERATOR = Path(COCCI_DIR / "conditional_operator.cocci")
    IMPLICIT_PREDICATE = Path(COCCI_DIR / "implicit_predicate.cocci")
    LOGIC_AS_CONTROLFLOW = Path(COCCI_DIR / "logic_as_controlflow.cocci")
    MACRO_OPERATOR_PRECEDENCE = Path(COCCI_DIR / "macro_operator_precedence.cocci")
    OMITTED_CURLY_BRACES = Path(COCCI_DIR / "omitted_curly_braces.cocci")
    OPERATOR_PRECEDENCE = Path(COCCI_DIR / "operator_precedence.cocci")
    POST_INCDEC = Path(COCCI_DIR / "post_incdec.cocci")
    PRE_INCDEC = Path(COCCI_DIR / "pre_incdec.cocci")
    REPURPOSED_VARIABLE = Path(COCCI_DIR / "repurposed_variable.cocci")
    REVERSED_SUBSCRIPT = Path(COCCI_DIR / "reversed_subscripts.cocci")
    TYPE_CONVERSION = Path(COCCI_DIR / "type_conversion.cocci")

    @staticmethod
    def from_string(value):
        patch_mapping = {patch.name.lower(): patch for patch in CocciPatch}
        # Lookup the enum member from the mapping
        enum_member = patch_mapping[value.lower()]
        return enum_member



# in some cases, subexpressions should be counted as separate atoms, in others, it seems unnecessary
remove_subexpressions_patches = (CocciPatch.ASSIGNMENT_AS_VALUE, CocciPatch.COMMA_OPERATOR, CocciPatch.TYPE_CONVERSION)
include_headers_patches = (CocciPatch.COMMA_OPERATOR, CocciPatch.MACRO_OPERATOR_PRECEDENCE)


def _check_if_subexpression(start_line, start_col, end_line, end_col, processed):
    new_range = {'start_line': int(start_line), 'start_col': int(start_col), 'end_line': int(end_line), 'end_col': int(end_col)}
    if start_line in processed:
        subset = any(_is_subset(new_range, existing) for existing in processed[start_line])
        if not subset:
            processed[start_line].append(new_range)
            processed[start_line] = [existing for existing in processed[start_line] if not _is_subset(existing, new_range)]
            return False
        else:
            return True
    else:
        processed[start_line] = [new_range]
        return False

def _is_subset(current, previous):
    # Check if the current range is entirely within the previous range
    if (current['start_line'] > previous['start_line'] or
        (current['start_line'] == previous['start_line'] and current['start_col'] >= previous['start_col'])) and \
       (current['end_line'] < previous['end_line'] or
        (current['end_line'] == previous['end_line'] and current['end_col'] <= previous['end_col'])):
        return True
    return False


def run_cocci(cocci_patch_path, c_input_path, output_file=None, opts=None):
    # keep all paths for this file to avoid additional imports from pathlib
    logging.debug(f"Running patch: {cocci_patch_path} against {c_input_path}")
    try:
        opts = opts or []
        if cocci_patch_path in [patch.value for patch in include_headers_patches]:
            opts.append("--include-headers")

        cmd = ["spatch","--jobs 4", "--sp-file", str(cocci_patch_path), str(c_input_path)] + opts
        print(cmd)
        if output_file is not None:
            output_file.touch()
            cmd.append(">>")
            cmd.append(str(output_file))
        run(cmd)

    except subprocess.CalledProcessError as e:
        raise RunCoccinelleError(f"An error occurred while running patch {cocci_patch_path}: {e}")


def read_csv_generator(file_path):
    with open(file_path, 'r', newline='', encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            yield row


def postprocess_and_generate_output(file_path: Path,  patch: CocciPatch, remove_end_line_and_col=True):
    seen = set() 
    filtered_data = [] 
    removed_lines_count = 0
    processed = {}
    logging.debug("Posptocessing: removing duplicate lines")

    previous_debug_row = None
    for row in read_csv_generator(file_path):
        key = tuple(row[1:-1])
        if row[0].startswith("Rule"):
            previous_debug_row = row
            continue

        if len(row) < 7:
            filtered_data.append(row)
            continue
        _, _, start_line, start_col, end_line, end_col, _ = row
        if key not in seen and (patch not in remove_subexpressions_patches or not _check_if_subexpression(start_line, start_col, end_line, end_col, processed)):
            if previous_debug_row is not None:
                filtered_data.append(previous_debug_row)
            seen.add(key)

            # remove end line and column from the final ouptut
            if remove_end_line_and_col:
                row = row[:4] + row[6:]
            filtered_data.append(row)

        else:
            removed_lines_count += 1
            previous_debug_row = None

    logging.debug(f"Removed {removed_lines_count} lines")
    return filtered_data


def run_patches_and_generate_output(input_path: Path, output_path: Optional[Path] = None, temp_dir: Optional[Path] = None, split_output = True, patch: Optional[CocciPatch] = None,  patches_to_skip: Optional[list] = None, remove_end_line_and_col=True):
    logging.debug("Running patches")
    if patch is None:
        # run all patche, except for patches to skip
        patches_to_run = [cocci_patch.value for cocci_patch in CocciPatch if cocci_patch not in patches_to_skip]
    else:
        patches_to_run = [patch.value]

    delete_temp = temp_dir is None
    all_atoms = []
    if temp_dir is None:
        temp_dir = tempfile.mkdtemp()

    def _write_lines_to_file(file_path, data_list):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write each row to the CSV file
            for row in data_list:
                writer.writerow(row)

    for patch_to_run in patches_to_run:
        temp_output_file = Path(temp_dir, f"{patch_to_run.stem}.csv")
        try:
            run_cocci(patch_to_run, input_path, output_file=temp_output_file)
        except RunCoccinelleError as e:
            # log the error and continue
            logging.error(str(e))
        
        atoms = postprocess_and_generate_output(temp_output_file, patch, remove_end_line_and_col)
        if split_output:
            output_file = output_path / f"{patch_to_run.stem}.csv"
            _write_lines_to_file(output_file, atoms)
        else:
            all_atoms.extend(atoms)
    
    if not split_output:
        _write_lines_to_file(output_path, all_atoms)

    if delete_temp:
        shutil.rmtree(temp_dir)
