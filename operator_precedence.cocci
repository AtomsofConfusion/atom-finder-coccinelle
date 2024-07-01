@rule1@
position p;
binary operator b1 = {+, -};
binary operator b2 = {*, /};
expression e1, e2;
identifier i;
constant c, c1, c2;
expression E;
@@

(
e1 +@E@p c b2 e2
|
e1 b2 c +@E@p e2
)

@script:python@
//b1 << rule1.b1;
//b2 << rule1.b2;
E << rule1.E;
p << rule1.p;
@@

print(f"Rule1:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")
//print(f"    b1: {b1}")
//print(f"    b2: {b2}")