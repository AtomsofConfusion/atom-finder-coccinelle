@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "literal-encoding"


def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col},\"{exp}\"")


def is_not_an_atom(n):
    # if < 8 (same representation as the corresponding octal number)
    # or 2 ^ n or 2 ^ n - 1
    # it is not an atom
    if n < 8:
        return True
    return (n & (n + 1)) == 0 or (n & (n - 1)) == 0


@rule01@
position p;
constant c1 !~ "^0.*", c2 !~ "^0.*";
binary operator bop = {^, &, |, <<, >>};
expression E;
@@

c1 bop@E@p c2


@script:python@
c1 << rule01.c1;
c2 << rule01.c2;
E << rule01.E;
p << rule01.p;
@@

try:
    n1 = int(c1)
    n2 = int(c2)
    if not is_not_an_atom(n1) or not is_not_an_atom(n2):
        print_expression_and_position(E, p, "Rule 01")
except ValueError:
    pass


@rule02@
position p;
constant c !~ "^0.*";
constant c1 =~ "^0.*";
identifier var;
binary operator bop = {^, &, |, <<, >>};
expression E;
@@

(
c bop@E@p c1
|
c1 bop@E@p c
|
c bop@E@p var
|
var bop@E@p c
)


@script:python@
c << rule02.c;
E << rule02.E;
p << rule02.p;
@@

try:
    n = int(c)
    if not is_not_an_atom(n):
        print_expression_and_position(E, p, "Rule 02")
except ValueError:
    pass



@rule11@
position p;
constant c !~ "^0.*";
expression e;
binary operator bop = {^, &, |, <<, >>};
expression E;
@@

(
~c bop@E@p e
|
e bop@E@p ~c
|
c bop@E@p e
|
e bop@E@p c
)

@script:python@
c << rule11.c;
E << rule11.E;
p << rule11.p;
@@


try:
    n = int(c)
    if not is_not_an_atom(n):
        print_expression_and_position(E, p, "Rule 11")
except ValueError:
    pass


@rule12@
position p;
constant c !~ "^0.*";
constant c1, c2;
expression e1, e2;
binary operator bop1 = {^, &, |, <<, >>}, bop2 = {^, &, |, <<, >>};
expression E;
@@

(
c1 bop1 c bop2@E@p c2;
|
e1 bop1@E@p ~c bop2 e2
|
e1 bop1 c bop2@E@p e2
)

@script:python@
c << rule12.c;
E << rule12.E;
p << rule12.p;
@@


try:
    n = int(c)
    if not is_not_an_atom(n):
        print_expression_and_position(E, p, "Rule 12")
except ValueError:
    pass


@rule2@
position p;
constant c !~ "^0.*";
expression e;
assignment operator aop = {^=, |=, &=, <<=, >>=};
expression E;
@@

(
e aop@E@p c
)

@script:python@
c << rule2.c;
E << rule2.E;
p << rule2.p;
@@


try:
    n = int(c)
    if not is_not_an_atom(n):
        print_expression_and_position(E, p, "Rule 2")
except ValueError:
    pass


@rule3@
position p;
constant c !~ "^0.*";
binary operator bop;
expression e;
@@

(
~ c@p
|
e bop ~ c@p
)

@script:python@
c << rule3.c;
p << rule3.p;
@@

try:
    n = int(c)
    if not is_not_an_atom(n):
        print_expression_and_position(f'~{c}', p, "Rule 3")
except ValueError:
    pass