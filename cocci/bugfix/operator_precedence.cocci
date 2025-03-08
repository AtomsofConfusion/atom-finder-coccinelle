@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "operator-precedence"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path}, {start_line}, {start_col}, \"{exp}\"")

@rule1@
position p;
binary operator b1 = {&, |, ^, <<, >>};
expression e1, e2;
expression E;
@@

(
  ! e1 b1@E@p e2
|
  ~ e1 b1@E@p e2
)

@script:python@
E << rule1.E;
p << rule1.p;
@@
print_expression_and_position(E, p, "Rule1")


@rule2@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, &, ^, |};
expression e1, e2, e3, e4;
expression E;
@@

(
  e1 b1 e2 ?@E@p e3 : e4
)

@script:python@
E << rule2.E;
p << rule2.p;
@@
print_expression_and_position(E, p, "Rule2")


@rule3@
position p;
binary operator b1 = {<<, >>};
expression e1, e2, e3;
expression E;
@@

(
  e1 b1 e2 &@E@p e3
|
  e1 b1 e2 |@E@p e3
|
  e1 b1 e2 ^@E@p e3
|
  e1 b1@E@p e2 * e3
|
  e1 * e2 b1@E@p e3
)


@script:python@
E << rule3.E;
p << rule3.p;
@@
print_expression_and_position(E, p, "Rule3")
