@script:python@
@@
mySet = set()

@rule1@
expression e1, e2;
expression E;
position p;
@@

e1 ,@E@p e2

@script:python@
p << rule1.p;
@@

if p[0].line not in mySet:
  print(f"Rule1: Line {p[0].line} in file {p[0].file}")
  mySet.add(p[0].line)