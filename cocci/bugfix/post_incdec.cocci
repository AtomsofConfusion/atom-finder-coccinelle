@script:python@
@@
from pathlib import Path
debug = False
ATOM_NAME = "post-increment"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col},\"{exp}\"")


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
...
( 
    var->arr[e]
| 
    arr[e]
|
    fun(..., e, ...)
)
...
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
binary operator bop1, bop2;
assignment operator aop;
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
return e;
|
return e3 bop1 e;
|
return e bop1 e3;
|
return e3 bop1 e bop2 e4;
|
for (e = e1;...;...) s
|
e aop e3
|
e < 0
|
e == -1
|
e@p2
)


@script:python@
p << rule2.p;
p2 << rule2.p2;
E << rule2.E;
@@

if p2[0].line > p[0].line:
    print_expression_and_position(E, p, "Rule 2")
