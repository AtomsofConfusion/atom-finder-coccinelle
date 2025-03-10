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
