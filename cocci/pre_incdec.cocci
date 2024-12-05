@script:python@
@@
from pathlib import Path
debug = False
ATOM_NAME = "pre-increment"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col}\"{exp}\"")


@non_atoms@
expression e,x;
statement S;
type t;
identifier i;
position p;
@@

(
 ++e@p;
|
for(...;...;++e@p) S
|
for(t i = x;...;++e@p) S
|
 --e@p;
|
for(...;...;--e@p) S
|
for(t i = x;...;--e@p) S
)

@rule1@
expression e;
position p1 != non_atoms.p;
position p;
expression E;
@@

(
 ++e@p1 @E@p
|
 --e@p1 @E@p
)

@script:python@
p << rule1.p;
E << rule1.E;
@@

print_expression_and_position(E, p, "Rule 1")
