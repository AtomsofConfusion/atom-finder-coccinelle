@r@
expression e1, e2;
position p;
@@

(
e1 && e2@p;
|
e1 || e2@p;
)

@script:python@
p << r.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")