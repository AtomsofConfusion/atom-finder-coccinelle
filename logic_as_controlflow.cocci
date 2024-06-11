@rule1@
expression e, e1, e2;
expression E;
binary operator bop1 = {&&, ||}, bop2 = {&&, ||};
identifier i;
position p;
@@

(
e bop1@E@p i++
|
e bop1@E@p i--
|
e1 bop1@E@p i++ bop2 e2
|
e1 bop1@E@p i-- bop2 e2
)

@script:python@
E << rule1.E;
p << rule1.p;
@@

print("Rule1: ")
print(f"   E:  {E}")
print(f"       Line: {p[0].line}, Col: {p[0].column} - {p[0].column_end}")

@rule2@
expression e, e1, e2;
expression E;
binary operator bop1 = {&&, ||}, bop2 = {&&, ||};
unary operator uop = {++, --};
identifier i;
position p;
@@

(
e bop1@E@p uop i
|
e bop1@E@p uop i
|
e1 bop1@E@p uop i bop2 e2
|
e1 bop1@E@p uop i bop2 e2
)

@script:python@
E << rule1.E;
p << rule1.p;
@@

print("Rule2: ")
print(f"   E:  {E}")
print(f"       Line: {p[0].line}, Col: {p[0].column} - {p[0].column_end}")