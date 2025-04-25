@script:python@
@@
from pathlib import Path
debug = False
ATOM_NAME = "post-increment"

def print_expression_and_position(exp, position, position2, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    p1_line, p1_col = position[0].line, position[0].column
    p2_line, p2_col = position2[0].line, position2[0].column

    print(f"{ATOM_NAME},{file_path},{p1_line},{p1_col},{p2_line},{p2_col},\"{exp}\"")


@rule1@
expression e, e1, e2, E;
binary operator b1 = {&&, ||}, b2 = {&&, ||};
position p;
identifier arr, var, fun; 
@@

while (
(
    e-- @E@p >= 0 
|
    e1 b1 (e-- @E@p >= 0)
|
    (e--  @E@p >= 0) b1 e1
|
    e1 b1 (e-- @E@p >= 0)  b2 e2
) )
{ 
<+...
( 
    var->arr[e]
| 
    arr[e]
)
...+>
}

@script:python@
p << rule1.p;
E << rule1.E;
@@

print_expression_and_position(E, p, "Rule 1")



@rule2@
position p, p2;
type t = unsigned;
expression e, E, e1, e2, e3, e4;
statement S, s;
binary operator b1 = {&&, ||}, b2 = {&&, ||};
binary operator b3 = {&&, ||}, b4 = {&&, ||};
assignment operator aop;
iterator iter;
identifier fun;
@@

while (
(
    e-- @E@p
|
    e1 b1 (e-- @E@p)
|
    (e-- @E@p) b1 e1
|
    e1 b1 ((e-- @E@p))  b2 e2
) ) S
...
(
for (e = e1;...;...) s
|
e--
|
e++
|
iter(..., e, ...) { ... }
|
e aop e3
|
(
if (
(
    e@p2
|
    e@p2 == 0
|
    e3 b3 e@p2
|
    e3 b3 !e@p2
|
    e3 b3 e@p2 == 0
|
    e@p2 b3 e3
|
    e@p2 == 0 b3 e3
|
    e3 b3 e@p2 b4 e4
|
    e3 b3 !e@p2 b4 e4
|
    e3 b3 e@p2 == 0 b4 e4
))
s
)
)


@script:python@
p << rule2.p;
p2 << rule2.p2;
E << rule2.E;
@@

if p2[0].line > p[0].line:
    print_expression_and_position(E, p, p2, "Rule 2")
