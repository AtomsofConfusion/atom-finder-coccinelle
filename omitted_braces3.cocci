@r3 disable braces0@
statement S;
position p;
expression e;
@@
(
while(...) {...}
|
while(...) S@p
)

@script:python@
p << r3.p;
@@
print(f"R3: Line {p[0].line} in file {p[0].file}")
