@script:python@
@@
from pathlib import Path
debug = False
ATOM_NAME = "post-increment"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
      print(rule_name)
    if position[0].line == position[0].line_end:
        print(f"{ATOM_NAME}, {file_path}, {position[0].line}: {position[0].column} - {position[0].column_end}, \"{exp}\"")
    else:
        position_start = f"{position[0].line}: {position[0].column}"
        position_end = f"{position[0].line_end}: {position[-1].column_end}"
        print(f"{ATOM_NAME}, {file_path}, {position_start} - {position_end} \"{exp}\"")

@non_atoms@
expression e,x;
statement S;
type t;
identifier i;
position p;
@@

(
e@p++;
|
for(...;...;e@p++) S
|
for(t i = x;...;e@p++) S
|
e@p--;
|
for(...;...;e@p--) S
|
for(t i = x;...;e@p--) S
)

@rule1@
expression e, E;
position p1 != non_atoms.p;
position p;
@@

(
e@p1++ @E@p
|
e@p1-- @E@p
)

@script:python@
p << rule1.p;
E << rule1.E;
@@

print_expression_and_position(E, p, "Rule 1")
