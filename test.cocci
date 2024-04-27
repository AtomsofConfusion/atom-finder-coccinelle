@test1@ 
expression e, e1, e2;
position p, p1, p2;
constant c;
identifier i, i1, i2;
statement s;
@@ 

// for the "else if" sequences between "if" and "else"
(
  if (...) {...}
  else if (...)@p {...}
  else {...}
)

@script:python@
p << test1.p;
@@

print(f"Test1 Matchings: Line {p[0].line} in file {p[0].file}.")

@test2@
expression e;
position p;
constanc c;
identifier i;
statement s;
@@

// this can match all the else if and else
(
  if (...) {...}
  else@p {...}
)

@script:python@
p << test2.p;
@@

print(f"Test2 Matchings: Line {p[0].line} in file {p[0].file}.")