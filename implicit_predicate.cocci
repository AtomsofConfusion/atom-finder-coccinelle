@script:python@
@@
from pathlib import Path
debug = False
ATOM_NAME = "implicit-predicate"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    print(f"{ATOM_NAME},{file_path},{position[0].line},{position[0].column},\"{exp}\"")

@rule01@
expression e1, e2;
expression E;
binary operator bop = {>, <, >=, <=, ==, !=};
position p;
@@

e1 bop@E@p e2

@rule1@
expression e;
statement s1, s2;
statement S;
position p != {rule01.p};
@@

if (e@S@p) s1 else s2

@script:python@
p << rule1.p;
S << rule1.S;
@@

print_expression_and_position(S, p, "Rule 1")

@rule2@
expression e;
position p != {rule01.p};
statement s;
statement S;
@@

(
while (e@S@p) s
|
do s while (e@S@p);
|
for (...;e@S@p;...) s
)

@script:python@
p << rule2.p;
S << rule2.S;
@@

print_expression_and_position(S, p, "Rule 2")

@rule3@
expression e, ec, el, er;
position p != {rule01.p};
statement S;
@@

ec@S@p ? el : er 

@script:python@
p << rule3.p;
S << rule3.S;
@@

print_expression_and_position(S, p, "Rule 3")