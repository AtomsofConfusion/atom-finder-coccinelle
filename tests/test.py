import pytest
import pandas as pd
from pandas import read_csv
from pathlib import PurePath

from src.run_cocci import run_cocci

### Modify this later
patch_to_input_mapping = {
    "assignment_as_value.cocci": ["assignment_as_value.c", "assignment_as_value.csv"],
    "change_of_literal_encoding.cocci": ["change_of_literal_encoding.c", "change_of_literal_encoding.csv"],
    "comma_operator.cocci": ["comma_operator.c", "comma_operator.csv"],
    "conditional_operator.cocci": ["conditional_operator.c", "conditional_operator.csv"],
    "implicit_predicate.cocci": ["implicit_predicate.c", "implicit_predicate.csv"],
    "logic_as_controlflow.cocci": ["logic_as_controlflow.c", "logic_as_controlflow.csv"],
    # "macro_operator_precedence.cocci": [".c"],
    "omitted_curly_braces.cocci": ["omitted_curly_braces.c", "omitted_curly_braces.csv"],
    # "operator_precedence.cocci": [".c"],
    "post_incdec.cocci": ["post_incdec.c", "post_incdec.csv"],
    "pre_incdec.cocci": ["pre_incdec.c", "pre_incdec.csv"],
    # "repurposed_variable.cocci": ["repurposed_variable.c", "repurposed_variable.csv"],
    # "reversed_subscripts.cocci": ["reversed_subscripts.c", "reversed_subscripts.csv"],
    # "type_conversion.cocci": ["type_conversion.c", "type_conversion.csv"],
}

working_dir = PurePath("../")
patch_path = working_dir / "cocci"
input_path = working_dir / "tests/data/inputs"
expected_path = working_dir / "tests/data/expected_outputs"

def compare(patch):
    try:
        data = run_cocci(["--quiet"], patch_path / patch, input_path / patch_to_input_mapping[patch][0])

        expected = expected_path / patch_to_input_mapping[patch][1]
        
        output = read_csv(data, header=None) # turns StringIO result into dataframe
        
        expected = read_csv(expected, header=None)
        
        expected = expected.iloc[:,[2,4]]
        output = output.iloc[:,[2,4]]

        for i in range(len(output)):
            output.iloc[i,1] = output.iloc[i,1].replace(' ', '')

        output = output.groupby(2)[4].apply(list).reset_index()
        expected = expected.groupby(2)[4].apply(list).reset_index()
        combined = pd.merge(expected, output, on=2, suffixes=('_1', '_2'), how="outer")

        combined = combined.fillna(pd.NA) # otherwise the next line won't work
        combined = combined.map(lambda x: [] if x is pd.NA else x)

        combined.to_csv(working_dir / "tests/debug.csv", index=False)
        # strings1 should be expected, and s2 is output
        def is_contained(strings1, strings2):
            set1 = set(strings1)
            set2 = set(strings2)
            return set1 == set2
            # return (len(set1)==len(set2))&all(any(s1 in s2 for s1 in set1) for s2 in set2)
        
        combined['Containment'] = combined.apply(lambda row: is_contained(row['4_1'], row['4_2']), axis=1)        
        is_equal = combined['Containment'].all()
        return is_equal
    
    except Exception as e:
        print(f"Something else happened: {e}, for {input}")

# individual tests
def test_assignment_as_value():
    patch = "assignment_as_value.cocci"
    result = compare(patch)
    assert(result == True)

def test_change_of_literal_encoding():
    patch = "change_of_literal_encoding"
    result = compare(patch)
    assert(result == True)

def test_comma_operator():
    patch = "comma_operator.cocci"
    result = compare(patch)
    assert(result == True)

def test_conditional_operator():
    patch = "conditional_operator.cocci"
    result = compare(patch)
    assert(result == True)
    
def test_implicit_predicate():
    patch = "implicit_predicate.cocci"
    result = compare(patch)
    assert(result == True)

def test_logic_as_controlflow():
    patch = "logic_as_controlflow.cocci"
    result = compare(patch)
    assert(result == True)

def test_omitted_curly_braces():
    patch = "omitted_curly_braces.cocci"
    result = compare(patch)
    assert(result == True)

def test_post_incdec():
    patch = "post_incdec.cocci"
    result = compare(patch)
    assert(result == True)

def test_pre_incdec():
    patch = "pre_incdec.cocci"
    result = compare(patch)
    assert(result == True)

# def test_repurposed_variable():
#     patch = "repurposed_variable.cocci"
#     result = compare(patch)
#     assert(result == True)

# def test_reversed_subscripts():
#     patch = "reversed_subscripts.cocci"
#     result = compare(patch)
#     assert(result == True)

# def test_type_conversion():
#     patch = "type_conversion.cocci"
#     result = compare(patch)
#     assert(result == True)

def initialize_test():
    pytest.main()
