@script:python@
@@
filtered = []

def is_subset(exp1, exp2):
    return (exp1['line'] == exp2['line'] and
            exp1['col_start'] >= exp2['col_start'] and
            exp1['col_end'] <= exp2['col_end'])

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
e1 bop1 c bop2@E@p e2
|
c bop@E@p e
|
e bop@E@p c
|
e1 bop1@E@p ~c bop2 e2
|
~c bop@E@p e
|
e bop@E@p ~c
)

@script:python@
c << rule1.c;
E << rule1.E;
p << rule1.p;
@@

n = int(c)

if not (n > 0 and (n & (n - 1)) == 0):
    line_number = p[0].line
    col_start = p[0].column
    col_end = p[0].column_end
    exp = {'line': line_number, 'col_start': col_start, 'col_end': col_end, 'expression': str(E)}

    should_add = True;
    to_remove = [];
    for f in filtered:
        if is_subset(exp, f):
            should_add = False
            break
        if is_subset(f, exp):
            to_remove.append(f)
            
    if should_add:
        filtered = [f for f in filtered if f not in to_remove]
        filtered.append(exp)

@script:python@
@@

for exp in filtered:
    print("Rule1: ")
    print(f"   E:  {exp['expression']}")
    print(f"       Line: {exp['line']}, Col: {exp['col_start']} - {exp['col_end']}")

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

if not (n > 0 and (n & (n - 1)) == 0):
    print("Rule2: ")
    print(f"   E:  {E}")
    print(f"       Line: {p[0].line}, Col: {p[0].column} - {p[0].column_end}")

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

if not (n > 0 and (n & (n - 1)) == 0):
    print("Rule3: ")
    print(f"   E:  ~ {c}")
    print(f"       Line: {p[0].line}, Col: {p[0].column} - {p[0].column_end}")