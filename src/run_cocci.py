import csv
import tempfile
from enum import Enum
from pathlib import Path
from subprocess import run, PIPE, CalledProcessError
from typing import Optional, Dict
from io import StringIO
from sys import stderr

from src import COCCI_DIR
from src.log import logging
from src.exceptions import RunCoccinelleError


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


def find_atoms(
    input_path: Path, output: Optional[Path] = None, patch: Optional[CocciPatch] = None
) -> Dict[CocciPatch, str]:
    if patch is None:
        # run all patche
        patches_to_run = [cocci_patch.value for cocci_patch in CocciPatch]
    else:
        patches_to_run = [patch]

    all_atoms = {}
    for patch_to_run in patches_to_run:
        atoms = run_cocci(patch_to_run, input_path)
        all_atoms[patch_to_run] = atoms

    return all_atoms


def run_cocci(cocci_patch_path, c_input_path, output_file=None, opts=None):
    # keep all paths for this file to avoid additional imports from pathlib
    logging.info(f"Running patch: {cocci_patch_path} against {c_input_path}")
    if opts is None:
        opts = []
    try:
        cmd = ["spatch", "--sp-file", str(cocci_patch_path), str(c_input_path)] + opts
        if output_file is not None:
            output_file.touch()
            cmd.append(">>")
            cmd.append(str(output_file))
        result = run(
            " ".join(cmd),
            shell=True,
            stderr=PIPE,
            stdout=PIPE,
            check=True,
            universal_newlines=True,
        )
        if output_file is None:
            output = result.stdout
            return output
        return None

    except CalledProcessError as e:
        raise RunCoccinelleError(f"An error occurred while running patch {cocci_patch_path}: {e.stderr.strip()}")


def read_csv_generator(file_path):
    with open(file_path, 'r', newline='', encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            yield row


def postprocess_and_generate_output(file_path: Path, output_file_path: Path):
    seen = set() 
    filtered_data = [] 
    removed_lines_count = 0
    logging.info("Posptocessing: removing duplicate lines")
    with open(output_file_path, mode='w', newline='', encoding="utf8") as outfile:
        writer = csv.writer(outfile)

        for row in read_csv_generator(file_path):
            key = tuple(row[1:-1])
            if key not in seen:
                seen.add(key)
                filtered_data.append(row)

                if len(filtered_data) > 10000: 
                    writer.writerows(filtered_data)
                    filtered_data.clear()
            else:
                removed_lines_count += 1
        if filtered_data:
            writer.writerows(filtered_data)
            filtered_data.clear()
        logging.info(f"Removed {removed_lines_count} lines")
        logging.info(f"Save output to {output_file_path}")


def run_patches_and_generate_output(input_path: Path, output_dir: Optional[Path] = None, patch: Optional[CocciPatch] = None):
    if patch is None:
        # run all patche
        patches_to_run = [cocci_patch.value for cocci_patch in CocciPatch]
    else:
        patches_to_run = [patch.value]
    with tempfile.TemporaryDirectory() as temp_dir:
        for patch_to_run in patches_to_run:
            temp_output_file = Path(temp_dir, f"{patch_to_run.stem}.csv")
            try:
                run_cocci(patch_to_run, input_path, output_file=temp_output_file)
            except RunCoccinelleError as e:
                # log the error and continue
                logging.error(str(e))
            output_file = output_dir / f"{patch_to_run.stem}.csv"
            postprocess_and_generate_output(temp_output_file, output_file)
