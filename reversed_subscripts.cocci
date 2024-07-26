@rule1@
position p;
expression E;
expression e;
identifier arr;
type ti = {int};
ti i;
constant c =~ "^[+-]?[1-9][0-9]*|0$";
constant str =~ "\"[^\"]*\"";
@@

(
  c[arr]@E@p
|
  c[str]@E@p
|
  i[arr]@E@p
|
  i[str]@E@p
)

@script:python@
p << rule1.p;
E << rule1.E;
@@

print(f"Rule1: ")
print(f"  line: {p[0].line}")
print(f"  E: {E}")