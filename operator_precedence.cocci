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

@rule51@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, ==, !=};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e &@E@p e2
)

@script:python@
E << rule51.E;
p << rule51.p;
@@

print(f"Rule5:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule61@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <, &};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e ^@E@p e2
)

@script:python@
E << rule61.E;
p << rule61.p;
@@

print(f"Rule6:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule71@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, &, ^};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e |@E@p e2
)

@script:python@
E << rule71.E;
p << rule71.p;
@@

print(f"Rule7:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule81@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, &, ^, |};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e &&@E@p e2
)

@script:python@
E << rule81.E;
p << rule81.p;
@@

print(f"Rule8:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule91@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, &, ^, &&};
expression e, e1, e2;
expression E;
@@

(
  e1 b1 e ||@E@p e2
)

@script:python@
E << rule91.E;
p << rule91.p;
@@

print(f"Rule9:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule101@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, &, ^, &&};
expression e1, e2;
expression t1, t2, t3;
expression E;
@@

(
  e1 b1 t1 ?@E@p t2 : t3
)

@script:python@
E << rule101.E;
p << rule101.p;
@@

print(f"Rule10:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

