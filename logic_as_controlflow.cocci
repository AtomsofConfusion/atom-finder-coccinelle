@r@
expression e1, e2;
position p;
@@

(
e1 && e2@p
|
e1 || e2@p
)

@script:python@
p << r.p;
e1 << r.e1;
@@

if "&&" not in e1 and "||" not in e1:
    print(f"Line {p[0].line} in file {p[0].file}")