import re
from collections import defaultdict


def compare(actual_rows, expected_rows):
    actual = _convert_to_dict(actual_rows)
    expected = _convert_to_dict(expected_rows)
    for line_and_offset, code_snippets in actual.items():
        if line_and_offset not in expected:
            assert False
        for code_snippet in code_snippets:
            assert code_snippet in expected[line_and_offset]
        assert len(code_snippets) == len(expected[line_and_offset])
    assert len(actual) == len(expected)


def _convert_to_dict(rows):
    line_code_mappings = defaultdict(list)
    for row in rows:
        if len(row) < 5:
            continue
        line = row[2]
        offset = row[3]
        code = row[4]
        if code.startswith('"'):
            code = code[1:-1]
        formatted_code = re.sub(r'\s+', '', code)
        line_code_mappings[(line, offset)].append(formatted_code)

    return line_code_mappings


