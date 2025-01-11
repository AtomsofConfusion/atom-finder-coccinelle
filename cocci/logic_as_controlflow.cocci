@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "logic-as-controlflow"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col},\"{exp}\"")


@rule01@
identifier fun;
identifier F;
expression e;
identifier i;
type t;
type t_a;
position p;
assignment operator aop;
@@

(
t fun@F@p (..., t_a *i,... ) {
  ...
  *i aop e
  ...
}
|
t fun@F@p (..., t_a *i,... ) {
  ...
  (*i)++
  ...
}
|
t fun@F@p (..., t_a *i,... ) {
  ...
  (*i)--
  ...
}
|
t fun@F@p (..., t_a *i,... ) {
  ...
  ++(*i)
  ...
}
|
t fun@F@p (..., t_a *i,... ) {
  ...
  --(*i)
  ...
}
)

@rule1@
expression e1, e2;
expression E;
binary operator bop = {&&, ||};
assignment operator aop;
identifier i;
position p;
@@

(
e1 bop@E@p <+... i++ ...+>
|
e1 bop@E@p <+... i-- ...+>
|
e1 bop@E@p <+... ++i ...+>
|
e1 bop@E@p <+... --i ...+>
|
e1 bop@E@p <+... i aop e2 ...+>
)

@script:python@
E << rule1.E;
p << rule1.p;
@@

//print("Rule1: ")
//print(f"   E:  {E}")
//print(f"       Line: {p[0].line}, Col: {p[0].column} - {p[0].column_end}")
print_expression_and_position(E, p)

@rule2@
position p;
binary operator bop = {||, &&};
identifier fun = rule01.F;
expression e;
expression E;
@@

(
e bop@E@p <+... fun(...) ...+>
)

@script:python@
E << rule2.E;
p << rule2.p;
@@

//print("Rule2: ")
//print(f"   E:  {E}")
//print(f"       Line: {p[0].line}, Col: {p[0].column} - {p[0].column_end}")
print_expression_and_position(E, p)
