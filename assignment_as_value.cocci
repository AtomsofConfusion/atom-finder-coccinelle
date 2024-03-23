@assignment_as_value@
expression e1, e2, e3;
position p;
@@


//e3 can be an assignemt or something else

e1=e2=e3@p


@script:python@
p << assignment_as_value.p;
e3 << assignment_as_value.e3;
@@

# this will deduplicate the matches
# if we have v1 = v2 = v3 = v4 = 10;
# e3 will be v3 = v4 = 10 (when e1 is v1 and e2 is v2)
# v4 = 10 (when e1 is v2 and e2 is v3)
# and finally, 10 (when e1 is v3, e2 is v4)

if ("=" not in e3):
    print(f"Line {p[0].line} in file {p[0].file}")


