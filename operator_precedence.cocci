@rule11@
position p;
binary operator b1 = {*, /, %};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e +@E@p e2
)

@script:python@
E << rule11.E;
p << rule11.p;
@@

print(f"Rule1:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule12@
position p;
binary operator b1 = {*, /, %};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e -@E@p e2
)

@script:python@
E << rule12.E;
p << rule12.p;
@@

print(f"Rule1:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule21@
position p;
binary operator b1 = {*, /, %, +, -};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e >>@E@p e2
)

@script:python@
E << rule21.E;
p << rule21.p;
@@

print(f"Rule2:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule22@
position p;
binary operator b1 = {*, /, %, +, -};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e <<@E@p e2
)

@script:python@
E << rule22.E;
p << rule22.p;
@@

print(f"Rule2:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule31@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e >@E@p e2
)

@script:python@
E << rule31.E;
p << rule31.p;
@@

print(f"Rule3:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule32@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e >=@E@p e2
)

@script:python@
E << rule32.E;
p << rule32.p;
@@

print(f"Rule3:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule33@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e <@E@p e2
)

@script:python@
E << rule33.E;
p << rule33.p;
@@

print(f"Rule3:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule34@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e <=@E@p e2
)

@script:python@
E << rule34.E;
p << rule34.p;
@@

print(f"Rule3:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule41@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e ==@E@p e2
)

@script:python@
E << rule41.E;
p << rule41.p;
@@

print(f"Rule4:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule42@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e !=@E@p e2
)

@script:python@
E << rule42.E;
p << rule42.p;
@@

print(f"Rule4:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule5@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, ==, !=};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e &@E@p e2
)

@script:python@
E << rule5.E;
p << rule5.p;
@@

print(f"Rule5:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule6@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <, &};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e ^@E@p e2
)

@script:python@
E << rule6.E;
p << rule6.p;
@@

print(f"Rule6:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule7@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, &, ^};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e |@E@p e2
)

@script:python@
E << rule7.E;
p << rule7.p;
@@

print(f"Rule7:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule8@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, &, ^, |};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e &&@E@p e2
)

@script:python@
E << rule8.E;
p << rule8.p;
@@

print(f"Rule8:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule9@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, &, ^, &&};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e ||@E@p e2
)

@script:python@
E << rule9.E;
p << rule9.p;
@@

print(f"Rule9:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule10@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, &, ^, &&};
expression e1, e2;
expression t1, t2;
expression E;
@@

(
  e1 b1 e2 ?@E@p t1 : t2
|
  t1 ?@E@p e1 b1 e2 : t2
|
  t1 ?@E@p t2 : e1 b1 e2
)

@script:python@
E << rule10.E;
p << rule10.p;
@@

print(f"Rule10:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

