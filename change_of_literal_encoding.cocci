@script:python@
@@
from pathlib import Path
processed = {}

def print_expression_and_position(exp, position):
    file_path = Path(position[0].file).resolve().absolute()
    if position[0].line == position[0].line_end:
        print(f"{file_path}, {position[0].line}: {position[0].column} - {position[0].column_end}, \"{exp}\"")
    else:
        position_start = f"{position[0].line}: {position[0].column}"
        position_end = f"{position[0].line_end}: {position[-1].column_end}"
        print(f"{file_path}, {position_start} - {position_end} \"{exp}\"")

def print_if_not_contained(exp, position):
    start_line, start_col = int(position[0].line), int(position[0].column)
    end_line, end_col = int(position[0].line_end), int(position[0].column_end)
    new_range = {'start_line': start_line, 'start_col': start_col, 'end_line': end_line, 'end_col': end_col}
    for line in range(start_line, end_line + 1):
        if line in processed:
            subset = any(is_contained(new_range, existing) for existing in processed[line])
            if not subset:
                processed[line].append(new_range)
                print_expression_and_position(exp, position)

        else:
          processed[line] = [new_range]
          print_expression_and_position(exp, position)

def is_contained(current, previous):
    # Check if the current range already added
    return current['start_line'] == previous['start_line'] and current['start_col'] == previous['start_col'] and \
        current['end_line'] == previous['end_line'] and current['end_col'] == previous['end_col']



def is_not_an_atom(n):
    # if < 8 (same representation as the corresponding octal number)
    # or 2 ^ n or 2 ^ n - 1
    # it is not an atom
    if n < 8:
        return True
    return (n & (n + 1)) == 0 or (n & (n - 1)) == 0

def get_range(position):
    line_number = int(p[0].line)
    start_line, start_col = int(position[0].line), int(position[0].column)
    end_line, end_col = int(position[0].line_end), int(position[0].column_end)
    new_range = {'start_line': start_line, 'start_col': start_col, 'end_line': end_line, 'end_col': end_col}
    return line_number, new_range


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

n1 = int(c1)
n2 = int(c2)

if is_not_an_atom(n1) and is_not_an_atom(n2):
    line_number, new_range = get_range(p)
    subset = False
    if line_number in processed:
        subset = any(is_contained(new_range, existing) for existing in processed[line_number])
    if not subset:
        processed.setdefault(line_number, []).append(new_range)

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

n = int(c)
if is_not_an_atom(n):
    line_number, new_range = get_range(p)
    subset = False
    if line_number in processed:
        subset = any(is_contained(new_range, existing) for existing in processed[line_number])
    if not subset:
        processed.setdefault(line_number, []).append(new_range)


@rule1@
position p;
constant c !~ "^0.*";
constant c1, c2;
expression e, e1, e2;
binary operator bop = {^, &, |, <<, >>};
binary operator bop1 = {^, &, |, <<, >>}, bop2 = {^, &, |, <<, >>};
expression E;
@@

(
c1 bop1 c bop@E@p c2;
|
e1 bop1@E@p ~c bop2 e2
|
~c bop@E@p e
|
e bop@E@p ~c
|
e1 bop1 c bop2@E@p e2
|
c bop@E@p e
|
e bop@E@p c
)

@script:python@
c << rule1.c;
E << rule1.E;
p << rule1.p;
@@


print_if_not_contained(E, p)

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

n = int(c)
if not is_not_an_atom(n):
    print_if_not_contained(E, p)

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

n = int(c)

if not is_not_an_atom(n):
    print_expression_and_position(f'~{c}', p)