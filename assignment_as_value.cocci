@initialize:python@
@@
unique = set()

@assignment_as_value@
expression e1, e2, e3;
position p;
@@

e1=e2=e3@p

//e3 can be an assignemt or something else
//do the same like in omitted braces
//v1 = v2 = v3 = 5; (5 is the value here)



@script:python@
p << assignment_as_value.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")

