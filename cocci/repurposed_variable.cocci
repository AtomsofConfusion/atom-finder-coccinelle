@script:python@
@@
from pathlib import Path
debug = False
ATOM_NAME = "repurposed_variable"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col}\"{exp}\"")


@rule1@
position p;
type tf, ti;
identifier fun, i;
assignment operator a;
expression e;
expression E;
@@

(
  tf fun(..., ti i, ...) {
    <+...
    i a@E@p e
    ...+>
  }
|
  tf fun(..., ti i, ...) {
    <+...
    i++@E@p
    ...+>
  }
|
  tf fun(..., ti i, ...) {
    <+...
    i--@E@p
    ...+>
  }
)


@script:python@
p << rule1.p;
E << rule1.E;
@@

print(f"Rule1: ")
print(f"  line: {p[0].line}")
print(f"  E: {E}")