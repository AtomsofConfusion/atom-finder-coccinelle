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
position p;
@@

e1 >@E@p e2

@rule02@
expression e1, e2;
expression E;
position p;
@@

e1 <@E@p e2

@rule03@
expression e1, e2;
expression E;
position p;
@@

e1 >=@E@p e2

@rule04@
expression e1, e2;
expression E;
position p;
@@

e1 <=@E@p e2

@rule05@
expression e1, e2;
expression E;
position p;
@@

e1 ==@E@p e2

@rule06@
expression e1, e2;
expression E;
position p;
@@

e1 !=@E@p e2

@rule1@
expression e;
statement s1, s2;
position p != {rule01.p, rule02.p, rule03.p, rule04.p, rule05.p, rule06.p};
@@

if (e@p) s1 else s2

@script:python@
p << rule1.p;
e << rule1.e;
@@

print_expression_and_position(e, p, "Rule 1")

@rule2@
expression e;
position p != {rule01.p, rule02.p, rule03.p, rule04.p, rule05.p, rule06.p};
@@

(
while (e@p) {...}
|
do {...} while (e@p);
|
for (...;e@p;...) {...}
)

@script:python@
p << rule2.p;
e << rule2.e;
@@

print_expression_and_position(e, p, "Rule 2")

@rule3@
expression e, ec, el, er;
position p != {rule01.p, rule02.p, rule03.p, rule04.p, rule05.p, rule06.p};
@@

ec@p ? el : er 

@script:python@
p << rule3.p;
ec << rule3.ec;
@@

print_expression_and_position(ec, p, "Rule 3")
