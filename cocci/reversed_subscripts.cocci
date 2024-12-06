@script:python@
@@
from pathlib import Path
debug = False
ATOM_NAME = "reversed_subscript"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col},\"{exp}\"")


@rule1@
position p;
expression E;
expression e;
identifier arr;
type ti = {int};
ti i;
constant c =~ "^[+-]?[1-9][0-9]*|0$";
constant str =~ "\"[^\"]*\"";
@@

(
  c[arr]@E@p
|
  c[str]@E@p
|
  i[arr]@E@p
|
  i[str]@E@p
)

@script:python@
p << rule1.p;
E << rule1.E;
@@

print_expression_and_position(E, p, "Rule 1")
