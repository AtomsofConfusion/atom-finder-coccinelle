import pandas as pd
from pathlib import Path
import unittest
from src.folder_check import check_all

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# two seperate mapping because there are more input .c files than .cocci patches
input_filenames = ['assignment_as_value.c', 'change_of_literal_encoding.c', 'comma_operator.c', 'conditional_operator.c', 'implicit_predicate.c', 'invalid_operator_precedence.c', 'macro_operator_precedence.c', 'logic_as_controlflow.c', 'macro_operator_precedence.c', 'macro_test.c','omitted_curly_braces.c', 'operator_precedence.c', 'post_incdec.c', 'pre_incdec.c', 'repurposed_variable.c', 'reversed_subscripts.c', 'type_conversion.c']

patch_filenames = ['assignment_as_value.cocci', 'change_of_literal_encoding.cocci', 'comma_operator.cocci', 'conditional_operator.cocci', 'implicit_predicate.cocci', 'macro_operator_precedence.cocci', 'logic_as_controlflow.cocci', 'omitted_curly_braces.cocci', 'operator_precedence.cocci', 'post_incdec.cocci', 'pre_incdec.cocci', 'repurposed_variable.cocci', 'reversed_subscripts.cocci', 'type_conversion.cocci']

cocci_patches_path = Path.cwd() / "cocci"
input_files_path = Path.cwd() / "tests/data/inputs"
cocci_outputs_path = Path.cwd() / "cocci_outputs"
expected_outputs_path = Path.cwd() / "tests/data/expected_outputs"

class Test(unittest.TestCase):
    def test_cocci_patch_complete(self):
        files_in_folder = [file.name for file in cocci_patches_path.iterdir() if file.is_file()]
        all_files_present = all(file in files_in_folder for file in patch_filenames)
        self.assertTrue(all_files_present)

    def test_c_inputs_complete(self):
        files_in_folder = [file.name for file in input_files_path.iterdir() if file.is_file()]
        all_files_present = all(file in files_in_folder for file in input_filenames)
        self.assertTrue(all_files_present)

    @unittest.expectedFailure
    def test_make_comparison(self):

        failed_cases = []

        for item in expected_outputs_path.glob("*.csv"):
            print(f"\n{item.name}:")

            output = pd.read_csv(Path(cocci_outputs_path, item.name), header=None)
            output = output.sort_values(by=output.columns[2])
            # output.to_csv()
            expected = pd.read_csv(Path(expected_outputs_path, item.name), header=None)

            line_numbers_output = output.iloc[:,2]
            line_numbers_expected = expected.iloc[:,2]
            
            missing_in_output = line_numbers_expected[~line_numbers_expected.isin(line_numbers_output)].tolist()
            missing_in_expected = line_numbers_output[~line_numbers_output.isin(line_numbers_expected)].tolist()

            print(f"Line numbers in expected but not in output:\n{missing_in_output}")
            print(f"Line numbers in output but not in expected:\n{missing_in_expected}")
                
            try:
                self.assertTrue(missing_in_output is None and missing_in_expected is None)
            except AssertionError as e:
                failed_cases.append(item.name)
        if failed_cases:
            print(f"\033[91m \n{len(failed_cases)} classes of atoms are incorrect.\033[0m")
        else:
            print(f"\033[92m \nAll cases passed.\033[0m")

# def run_tests():
#     check_all()
#     unittest.main()
