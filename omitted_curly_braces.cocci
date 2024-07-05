@script:python@
@@
from pathlib import Path
processed = {}
debug = True
ATOM_NAME = "omitted-curly-braces"

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

@r1 disable braces0, neg_if@ // this is disabling some isomorphisms
statement S, S1, S2;
position p;
@@

// first match the case that is not an atom, do not note the position
// then if that is not match, it will match the atom that is beneath it

(
if (...) {...} else S
|
if (...)@S@p S1 else S2
)

// write script right bellow the rule, 
@script:python@
p << r1.p;
S << r1.S;
@@
print_if_not_contained(S, p, "Rule 1")

@r2 disable braces0, neg_if@
statement S, S1, S2;
position p;
@@
(
if (...) S else {...}
|
if (...) S1 else @S@p S2@p
)
// here we have something where both rule 1 and 2 can match the same thing -> separate rules

@script:python@
p << r2.p;
S << r2.S;
@@
print_if_not_contained(S, p, "Rule 2")

@r3 disable braces0@
statement S, S1;
position p;
type t;
identifier i;
expression x;
@@
(
while(...) {...}
|
while(...)@S@p S1
|
for(t i = x;...;...) {...}
|
for(t i = x;...;...) @S@p S1
|
for(...;...;...) {...}
|
for(...;...;...) @S@p S1
|
do {...} while (...);
|
do S1 while (...) @S@p;
)

// for and while are separate things, no need for separate rules

@script:python@
p << r3.p;
S << r3.S;
@@
print_if_not_contained(S, p, "Rule 3")
