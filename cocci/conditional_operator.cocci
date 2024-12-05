@script:python@
@@
from pathlib import Path

ATOM_NAME = "conditional"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col}\"{exp}\"")


@rule1@
expression e, e1, e2;
expression E;
position p;
@@

e ?@E@p e1 : e2


@script:python@
p << rule1.p;
E << rule1.E;
@@

print_expression_and_position(E, p)