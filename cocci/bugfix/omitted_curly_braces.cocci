@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "omitted-curly-braces"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path}, {start_line}, {start_col}, \"{exp}\"")


@r1 disable braces0, neg_if@
statement S;
position p;
expression e1, e2, E;
@@


(
if (...) {...} else S
|
if (...) e1 ,@E@p e2; else S
)

// write script right bellow the rule, 
@script:python@
p << r1.p;
E << r1.E;
@@
print_expression_and_position(E, p, "Rule 1")

@r2 disable braces0, neg_if@
statement S;
position p;
expression e1, e2, E;
@@
(
if (...) S else {...}
|
if (...) S else e1 ,@E@p e2;
)

@script:python@
p << r2.p;
E << r2.E;
@@
print_expression_and_position(E, p, "Rule 2")

@r3 disable braces0@
statement S;
position p;
type t;
identifier i;
expression x, e1, e2, E;

@@
(
while(...) {...}
|
while(...) e1 ,@E@p e2;
|
for(t i = x;...;...) {...}
|
for(t i = x;...;...) e1 ,@E@p e2;
|
for(...;...;...) {...}
|
for(...;...;...) e1 ,@E@p e2;
)

@script:python@
p << r3.p;
E << r3.E;
@@
print_expression_and_position(E, p, "Rule 3")
