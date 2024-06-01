@script:python@
@@
from pathlib import Path

def print_expression_and_position(exp, position):
    file_path = Path(position[0].file).resolve().absolute()
    if position[0].line == position[0].line_end:
        print(f"{file_path}, {position[0].line}: {position[0].column} - {position[0].column_end}, \"{exp}\"")
    else:
        position_start = f"{position[0].line}: {position[0].column}"
        position_end = f"{position[0].line_end}: {position[-1].column_end}"
        print(f"{file_path}, {position_start} - {position_end} \"{exp}\"")

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