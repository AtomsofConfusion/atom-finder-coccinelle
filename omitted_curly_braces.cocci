
@r1 disable braces0, neg_if@ // this is disabling some isomorphisms
statement S, S1;
position p;
@@

// first match the case that is not an atom, do not note the position
// then if that is not match, it will match the atom that is beneath it

(
if (...) {...} else S
|
if (...) S@p else S1
)

// write script right bellow the rule, 
@script:python@
p << r1.p;
@@
print(f"R1: Line {p[0].line} in file {p[0].file}")

@r2 disable braces0, neg_if@
statement S, S1, S2;
position p;
@@
(
if (...) S else {...}
|
if (...) S else {
  ...
  if (...) S1 else S2
  ...
}
|
if (...) S else S1@p
)
// here we have something where both rule 1 and 2 can match the same thing -> separate rules

@script:python@
p << r2.p;
@@
print(f"R2: Line {p[0].line} in file {p[0].file}")

@r3 disable braces0@
statement S;
position p;
type t;
identifier i;
expression x;
@@
(
while(...) {...}
|
while(...) S@p
|
for(t i = x;...;...) {...}
|
for(t i = x;...;...) S@p
|
for(...;...;...) {...}
|
for(...;...;...) S@p
|
do {...} while (...);
|
do S@p while (...);
)

// for and while are separate things, no need for separate rules

@script:python@
p << r3.p;
@@
print(f"R3: Line {p[0].line} in file {p[0].file}")
