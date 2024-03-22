@initialize:python@
@@
unique = set()

@assignment_as_value@
expression e1, e2, e3;
position p;
@@

e1=e2=e3@p


@script:python@
p << assignment_as_value.p;
@@

if ((p[0].line, p[0].file)) not in unique:
    print(f"Line {p[0].line} in file {p[0].file}")
    unique.add((p[0].line, p[0].file))

