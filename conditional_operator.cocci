@conditional@
expression e1, e2, e3, e4;
identifier x;
type t;
position p;
@@

x = e1 == e2 ? e3 : e4 @p


@script:python@
p << conditional.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")
