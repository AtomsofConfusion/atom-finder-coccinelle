@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "omitted-curly-braces"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    print(f"{ATOM_NAME},{file_path},{position[0].line},{position[0].column},\"{exp}\"")


@r1 disable braces0, neg_if@
statement S, S1;
position p;
@@

// first match the case that is not an atom, do not note the position
// then if that is not match, it will match the atom that is beneath it


(
if (...) {...} else S1
|
if (...) S@p else S1
)

// write script right bellow the rule, 
@script:python@
p << r1.p;
S << r1.S;
@@
print_expression_and_position(S, p, "Rule 1")

@r2 disable braces0, neg_if@
statement S, S1;
position p;
@@
(
if (...) S1 else {...}
|
if (...) S1 else S@p
)

// here we have something where both rule 1 and 2 can match the same thing -> separate rules

@script:python@
p << r2.p;
S << r2.S;
@@
print_expression_and_position(S, p, "Rule 2")

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
print_expression_and_position(S, p, "Rule 3")