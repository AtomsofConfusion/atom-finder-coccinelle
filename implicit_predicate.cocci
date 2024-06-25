@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "implicit-predicate"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    print(f"{ATOM_NAME},{file_path},{position[0].line},{position[0].column},\"{exp}\"")

def print_if_not_contained(exp, position, rule_name=""):
    start_line, start_col = int(position[0].line), int(position[0].column)
    end_line, end_col = int(position[0].line_end), int(position[0].column_end)
    new_range = {'start_line': start_line, 'start_col': start_col, 'end_line': end_line, 'end_col': end_col}
    if start_line in processed:
        subset = any(is_subset(new_range, existing) for existing in processed[start_line])
        if not subset:
            processed[start_line].append(new_range)
            processed[start_line] = [existing for existing in processed[start_line] if not is_subset(existing, new_range)]
            print_expression_and_position(exp, position, rule_name)
    else:
        processed[start_line] = [new_range]
        print_expression_and_position(exp, position, rule_name)

def is_subset(current, previous):
    # Check if the current range is entirely within the previous range
    if (current['start_line'] > previous['start_line'] or
        (current['start_line'] == previous['start_line'] and current['start_col'] >= previous['start_col'])) and \
       (current['end_line'] < previous['end_line'] or
        (current['end_line'] == previous['end_line'] and current['end_col'] <= previous['end_col'])):
        return True
    return False

@rule01@
expression e1, e2;
expression E;
binary operator bop = {>, <, >=, <=, ==, !=};
position p;
@@

e1 bop@E@p e2

@rule1@
expression e;
statement s1, s2;
statement S;
position p1 != rule01.p;
position p;
@@

if (e@p1)@S@p s1 else s2

@script:python@
p << rule1.p;
S << rule1.S;
@@

print_if_not_contained(S, p, "Rule 1")

@rule2@
expression e;
position p1 != rule01.p;
position p;
statement s;
statement S;
@@

(
while (e@p1@S@p) s
|
do s while (e@p1); @S@p
|
for (...;e@p1@S@p;...) s
)

@script:python@
p << rule2.p;
S << rule2.S;
@@

print_if_not_contained(S, p, "Rule 2")

@rule3@
expression E;
expression ec, el, er;
position p1 != rule01.p;
position p;
statement S;
@@

ec@p1@E@p ? el : er 

@script:python@
p << rule3.p;
E << rule3.E;
@@

print_if_not_contained(E, p, "Rule 3")