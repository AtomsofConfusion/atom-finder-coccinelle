@rule1@
expression e, e1, e2;
expression E;
position p;
@@

e ?@E@p e1 : e2


@script:python@
p << rule1.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")