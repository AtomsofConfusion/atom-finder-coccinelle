@conditional@
expression e, e1, e2, e3, e4;
position p;
binary operator bop;
@@

e@p = e1 bop e2 ? e3 : e4


@script:python@
p << conditional.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")
