@r@
expression e, e1, e2;
position p;
@@

// this will also detect examples where we chain more expressions
// in that case e1 will include the all expression except for the last one
// whih will be included in e2
e = (e1, e2)@p

@script:python@
p << r.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")
