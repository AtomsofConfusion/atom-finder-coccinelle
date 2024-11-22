import pytest
import pandas as pd
from pandas import read_csv
from pathlib import Path

from src.run_cocci import run_cocci
from src.option_select import select

### Modify this later
patch_to_input_mapping = {
    "assignment_as_value.cocci": ["assignment_as_value.c"],
    "change_of_literal_encoding.cocci": ["change_of_literal_encoding.c"],
    "comma_operator.cocci": ["comma_operator.c"],
    "conditional_operator.cocci": ["conditional_operator.c"],
    "implicit_predicate.cocci": ["implicit_predicate.c"],
    "logic_as_controlflow.cocci": ["logic_as_controlflow.c"],
    # "macro_operator_precedence.cocci": [".c"],
    "omitted_curly_braces.cocci": ["omitted_curly_braces.c"],
    # "operator_precedence.cocci": [".c"],
    "post_incdec.cocci": ["post_incdec.c"],
    "pre_incdec.cocci": ["pre_incdec.c"],
    "repurposed_variable.cocci": ["repurposed_variable.c"],
    "reversed_subscripts.cocci": ["reversed_subscripts.c"],
    "type_conversion.cocci": ["type_conversion.c"],
}

### Modify this later
input_to_expected_mapping = {
    "assignment_as_value.c": "assignment_as_value.csv",
    "change_of_literal_encoding.c": "change_of_literal_encoding.csv",
    "comma_operator.c": "comma_operator.csv",
    "conditional_operator.c": "conditional_operator.csv",
    "implicit_predicate.c": "implicit_predicate.csv",
    # "invalid_operator_precedence.c": "invalid_operator_precedence.csv",
    "logic_as_controlflow.c": "logic_as_controlflow.csv",
    # "macro_operator_precedence.c": "macro_operator_precedence.csv",
    # "macro_test.c": "macro_test.csv",
    "omitted_curly_braces.c": "omitted_curly_braces.csv",
    # "operator_precedence.c": "operator_precedence.csv",
    "post_incdec.c": "post_incdec.csv",
    "pre_incdec.c": "pre_incdec.csv",
    "repurposed_variable.c": "repurposed_variable.csv",
    "reversed_subscripts.c": "reversed_subscripts.csv",
    "type_conversion.c": "type_conversion.csv",
}

patch_path = Path.cwd() / "cocci"
input_path = Path.cwd() / "tests/data/inputs"
expected_path = Path.cwd() / "tests/data/expected_outputs"

def compare(patch, input, verbosity):
    try:
        data = run_cocci(["--quiet"], patch_path / patch, input_path / input)

        expected = expected_path / input_to_expected_mapping[input]
        
        output = read_csv(data, header=None) # turns StringIO result into dataframe
        
        expected = read_csv(expected, header=None)
        
        expected = expected.iloc[:,[2,4]]
        output = output.iloc[:,[2,4]]

        for i in range(len(output)):
            output.iloc[i,1] = output.iloc[i,1].replace(' ', '')

        output = output.groupby(2)[4].apply(list).reset_index()
        expected = expected.groupby(2)[4].apply(list).reset_index()
        combined = pd.merge(expected, output, on=2, suffixes=('_1', '_2'), how="outer")

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)

        combined = combined.fillna(pd.NA) # otherwise the next line won't work
        combined = combined.map(lambda x: [] if x is pd.NA else x)

        combined.to_csv("tests/debug.csv", index=False)
        # strings1 should be expected, and s2 is output
        def is_contained(strings1, strings2):
            set1 = set(strings1)
            set2 = set(strings2)
            # return set1 == set2
            return (len(set1)==len(set2))&all(any(s1 in s2 for s1 in set1) for s2 in set2)
        
        combined['Containment'] = combined.apply(lambda row: is_contained(row['4_1'], row['4_2']), axis=1)        
        is_equal = combined['Containment'].all()
        return is_equal
    
    except Exception as e:
        print(f"Something else happened: {e}, for {input}")

# individual tests
@pytest.mark.parametrize("input", patch_to_input_mapping["assignment_as_value.cocci"])
def test_assignment_as_value(input):
    patch = "assignment_as_value.cocci"
    # missing_in_expected, missing_in_output = compare(patch, input, 0)
    result = compare(patch, input, 0)
    assert(result == True)
    # assert(not len(missing_in_output) and not len(missing_in_expected) == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["change_of_literal_encoding.cocci"])
def test_change_of_literal_encoding(input):
    patch = "change_of_literal_encoding.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["comma_operator.cocci"])
def test_comma_operator(input):
    patch = "comma_operator.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["conditional_operator.cocci"])
def test_conditional_operator(input):
    patch = "conditional_operator.cocci"
    result = compare(patch, input, 0)
    assert(result == True)
    
@pytest.mark.parametrize("input", patch_to_input_mapping["implicit_predicate.cocci"])
def test_implicit_predicate(input):
    patch = "implicit_predicate.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["logic_as_controlflow.cocci"])
def test_logic_as_controlflow(input):
    patch = "logic_as_controlflow.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["omitted_curly_braces.cocci"])
def test_omitted_curly_braces(input):
    patch = "omitted_curly_braces.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["post_incdec.cocci"])
def test_post_incdec(input):
    patch = "post_incdec.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["pre_incdec.cocci"])
def test_pre_incdec(input):
    patch = "pre_incdec.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["repurposed_variable.cocci"])
def test_repurposed_variable(input):
    patch = "repurposed_variable.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["reversed_subscripts.cocci"])
def test_reversed_subscripts(input):
    patch = "reversed_subscripts.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

@pytest.mark.parametrize("input", patch_to_input_mapping["type_conversion.cocci"])
def test_type_conversion(input):
    patch = "type_conversion.cocci"
    result = compare(patch, input, 0)
    assert(result == True)

### Modify this later
patch_to_test_mapping = {
    "assignment_as_value.cocci": "test_assignment_as_value",
    "change_of_literal_encoding.cocci": "test_change_of_literal_encoding",
    "comma_operator.cocci": "test_comma_operator",
    "conditional_operator.cocci": "test_conditional_operator",
    "implicit_predicate.cocci": "test_implicit_predicate",
    "logic_as_controlflow.cocci": "test_logic_as_controlflow",
    "omitted_curly_braces.cocci": "test_omitted_curly_braces",
    "post_incdec.cocci": "test_post_incdec",
    "pre_incdec.cocci": "test_pre_incdec",
    # "repurposed_variable.cocci": "test_repurposed_variable",
    # "reversed_subscripts.cocci": "test_reversed_subscripts",
    # "type_conversion.cocci": "test_type_conversion",
}

# patch file list from keyboard selection, call corresponding test functions (same name as patch) through args, append input files in for each pytest parameter,  
def initialize_test():
    select_list = []
    select_list = patch_to_test_mapping.keys()
    select_list = select(select_list)

    args = []
    for patch in select_list:
        args.append(f"tests/test.py::{patch_to_test_mapping[patch]}")
    pytest.main(args)
