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
    if position[0].line == position[0].line_end:
        print(f"{ATOM_NAME}, {file_path}, {position[0].line}: {position[0].column} - {position[0].column_end}, \"{exp}\"")
    else:
        position_start = f"{position[0].line}: {position[0].column}"
        position_end = f"{position[0].line_end}: {position[-1].column_end}"
        print(f"{ATOM_NAME}, {file_path}, {position_start} - {position_end} \"{exp}\"")

def print_if_not_contained(exp, position, rule_name=""):
    start_line, start_col = int(position[0].line), int(position[0].column)
    end_line, end_col = int(position[0].line_end), int(position[0].column_end)
    new_range = {'start_line': start_line, 'start_col': start_col, 'end_line': end_line, 'end_col': end_col}
    for line in range(start_line, end_line + 1):
        if line in processed:
            subset = any(is_subset(new_range, existing) for existing in processed[line])
            if not subset:
                processed[line].append(new_range)
                processed[line] = [existing for existing in processed[line] if not is_subset(existing, new_range)]
                print_expression_and_position(exp, position, rule_name)
        else:
          processed[line] = [new_range]
          print_expression_and_position(exp, position, rule_name)

def is_subset(current, previous):
    # Check if the current range is entirely within the previous range
    if (current['start_line'] > previous['start_line'] or
        (current['start_line'] == previous['start_line'] and current['start_col'] >= previous['start_col'])) and \
       (current['end_line'] < previous['end_line'] or
        (current['end_line'] == previous['end_line'] and current['end_col'] <= previous['end_col'])):
        return True
    return False

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

print_if_not_contained(d, p, "Rule 1")

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

print_if_not_contained(E, p, "Rule 2")

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

print_if_not_contained(d, p, "Rule 3")

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

print_if_not_contained(E, p, "Rule 4")

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

print_if_not_contained(E, p, "Rule 5")