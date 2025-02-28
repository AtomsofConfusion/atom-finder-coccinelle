@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "implicit-predicate"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col},\"{exp}\"")


@rule01@
expression e1, e2;
expression E;
binary operator bop = {>, <, >=, <=, ==, !=};
position p;
@@

e1 bop@E@p e2

@rule1@
expression e, E;
statement s1, s2;
position p1 != rule01.p;
position p;
@@

if (e@p1@E@p) s1 else s2


@script:python@
p << rule1.p;
E << rule1.E;
@@

print_expression_and_position(E, p, "Rule 1")



@rule2@
expression e;
position p1 != rule01.p;
position p;
statement s;
expression E;
@@

(
while (e@p1@E@p) s
|
do s while (e@E@p1);
|
for (...;e@p1@E@p;...) s
)

@script:python@
p << rule2.p;
E << rule2.E;
@@

print_expression_and_position(E, p, "Rule 2")


@rule3@
expression E;
expression ec, el, er;
position p1 != rule01.p;
position p;
statement S;
@@

ec@p1@E@p ? el : er 

@script:python@
p << rule3.p;
E << rule3.E;
@@

print_expression_and_position(E, p, "Rule 3")

