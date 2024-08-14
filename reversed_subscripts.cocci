@rule1@
position p;
expression E;
expression e1, e2, e3;
identifier arr;
type ti = {int};
ti i;
constant {ti} c;
constant str =~ "\"[^\"]*\"";
@@

(
  e1[arr[e2][e3]]@E@p
|
  e1[e2[arr[e3]]]@E@p
|
  e1[e2[e3[arr]]]@E@p
|
  e1[arr[e2]]@E@p
|
  e1[e2[arr]]@E@p
|
  e1[arr]@E@p
|
  e2[str]@E@p
)

@script:python@
p << rule1.p;
E << rule1.E;
@@

print(f"Rule1: ")
print(f"  line: {p[0].line}")
print(f"  E: {E}")