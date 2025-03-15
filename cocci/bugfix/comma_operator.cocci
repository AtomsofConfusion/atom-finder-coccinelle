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

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col},\"{exp}\"")


@r1 disable braces0, neg_if@
statement S;
position p, p1, p2;
expression e1, e2, E;
@@


(
if (...) {...} else S
|
if (...) e1@p1 ,@E@p e2@p2; else S
)

// write script right bellow the rule, 
@script:python@
p << r1.p;
E << r1.E;
p1 << r1.p1;
p2 << r1.p2;
@@

if p1[0].line_end != p2[0].line:
    print_expression_and_position(E, p, "Rule 1")

@r2 disable braces0, neg_if@
statement S;
position p, p1, p2;
expression e1, e2, E;
@@
(
if (...) S else {...}
|
if (...) S else e1@p1 ,@E@p e2@p2;
)

@script:python@
p << r2.p;
p1 << r2.p1;
p2 << r2.p2;
E << r2.E;
@@

if p1[0].line_end != p2[0].line:
    print_expression_and_position(E, p, "Rule 2")

@r3 disable braces0@
statement S;
position p, p1, p2;
type t;
identifier i;
expression x, e1, e2, E;

@@
(
while(...) {...}
|
while(...) e1@p1 ,@E@p e2@p2;
|
for(t i = x;...;...) {...}
|
for(t i = x;...;...) e1@p1 ,@E@p e2@p2;
|
for(...;...;...) {...}
|
for(...;...;...) e1@p1 ,@E@p e2@p2;
)

@script:python@
p << r3.p;
p1 << r3.p1;
p2 << r3.p2;
E << r3.E;
@@

if p1[0].line_end != p2[0].line:
    print_expression_and_position(E, p, "Rule 3")
