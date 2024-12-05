@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "assignment-as-value"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col}\"{exp}\"")

@rule1@
expression e1, e2;
position p;
identifier i;
assignment operator aop;
declaration d;
type t;
@@

(
t@d@p i = e1 aop e2;
|
t@d@p i = (e1 aop e2);
)


@script:python@
p << rule1.p;
d << rule1.d;
@@

print_expression_and_position(d, p, "Rule 1")

@rule2@
expression e1, e2, e3, e4;
assignment operator aop1, aop2;
binary operator bop;
expression E;
position p;
@@

(
e1 aop1@E@p e2 = e3
|
e1 aop1@E@p e2 += e3
|
e1 aop1@E@p e2 -= e3
|
e1 aop1@E@p e2 *= e3
|
e1 aop1@E@p e2 /= e3
|
e1 aop1@E@p e2 |= e3
|
e1 aop1@E@p e2 &= e3
|
e1 aop1@E@p (e2 aop2 e3)
|
e1 aop1@E@p e2 bop (e3 aop2 e4)
)


@script:python@
p << rule2.p;
E << rule2.E;
@@

print_expression_and_position(E, p, "Rule 2")

@rule3@
expression e1, e2;
position p;
declaration d;
assignment operator aop;
identifier i;
type t;
statement s;
@@

(
for (t@d@p i = e1 aop e2;...;...) s
|
for (t@d@p i = (e1 aop e2);...;...) s
)

@script:python@
d << rule3.d;
p << rule3.p;
@@

print_expression_and_position(d, p, "Rule 3")

@rule4@
expression e1, e2;
expression E;
assignment operator aop;
statement s;
position p;
@@

(
while (<+... e1 aop@E@p e2 ...+>) s
|
for (...;<+... e1 aop@E@p e2 ...+>;...) s
|
for (...;...;<+... e1 aop@E@p e2 ...+>) s
)

@script:python@
p << rule4.p;
E << rule4.E;
@@

print_expression_and_position(E, p, "Rule 4")

@rule5@
expression e1, e2;
expression E;
assignment operator aop;
statement s1, s2;
position p;
@@

if (<+... e1 aop@E@p e2 ...+>) s1 else s2

@script:python@
E << rule5.E;
p << rule5.p;
@@

print_expression_and_position(E, p, "Rule 5")