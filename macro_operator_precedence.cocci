@m_rule1@
expression e1, e2;
identifier m;
binary operator b = {*, /, %};
@@

#define m e1 b e2

@m_rule2@
expression e1, e2;
identifier m;
binary operator b = {+, -};
@@

#define m e1 b e2

@m_rule3@
expression e1, e2;
identifier m;
binary operator b = {<<, >>};
@@

#define m e1 b e2

@m_rule4@
expression e1, e2;
identifier m;
binary operator b = {<, <=, >, >=};
@@

#define m e1 b e2

@m_rule5@
expression e1, e2;
identifier m;
binary operator b = {==, !=};
@@

#define m e1 b e2

@m_rule6@
expression e1, e2;
identifier m;
binary operator b = {&};
@@

#define m e1 b e2

@m_rule7@
expression e1, e2;
identifier m;
binary operator b = {^};
@@

#define m e1 b e2

@m_rule8@
expression e1, e2;
identifier m;
binary operator b = {|};
@@

#define m e1 b e2

@m_rule9@
expression e1, e2;
identifier m;
binary operator b = {&&};
@@

#define m e1 b e2

@m_rule10@
expression e1, e2;
identifier m;
binary operator b = {||};
@@

#define m e1 b e2

@m_rule11@
expression e1, e2, e3;
identifier m;
@@

#define m e1 ? e2 : e3

@rule1@
position p;
expression e;
expression E;
identifier m = {m_rule10.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=, &, ^, |, &&};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule1.E;
p << rule1.p;
@@

print(f"Rule1:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule2@
position p;
expression e;
expression E;
identifier m = {m_rule9.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=, &, ^, |};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule2.E;
p << rule2.p;
@@

print(f"Rule2:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule3@
position p;
expression e;
expression E;
identifier m = {m_rule8.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=, &, ^};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule3.E;
p << rule3.p;
@@

print(f"Rule3:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule4@
position p;
expression e;
expression E;
identifier m = {m_rule7.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=, &};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule4.E;
p << rule4.p;
@@

print(f"Rule4:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule5@
position p;
expression e;
expression E;
identifier m = {m_rule6.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=};
@@

(
  m b@E@p e
|
  e b@E@p m
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
expression e;
expression E;
identifier m = {m_rule5.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=};
@@

(
  m b@E@p e
|
  e b@E@p m
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
expression e;
expression E;
identifier m = {m_rule4.m};
binary operator b = {*, /, %, +, -, <<, >>};
@@

(
  m b@E@p e
|
  e b@E@p m
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
expression e;
expression E;
identifier m = {m_rule3.m};
binary operator b = {*, /, %, +, -};
@@

(
  m b@E@p e
|
  e b@E@p m
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
expression e;
expression E;
identifier m = {m_rule2.m};
binary operator b = {*, /, %};
@@

(
  m b@E@p e
|
  e b@E@p m
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
expression e;
expression E;
identifier m = {m_rule1.m, m_rule2.m, m_rule6.m, m_rule9.m, m_rule10.m};
@@

(
  +@E@p m
|
  -@E@p m
)

@script:python@
E << rule10.E;
p << rule10.p;
@@

print(f"Rule10:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule11@
position p;
expression e;
expression E;
identifier m = {m_rule1.m, m_rule2.m, m_rule9.m, m_rule10.m, rule4.m, rule5.m};
@@

(
  !@E@p m
)

@script:python@
E << rule11.E;
p << rule11.p;
@@

print(f"Rule11:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule12@
position p;
expression e;
expression E;
identifier m = {m_rule2.m};
@@

(
  *@E@p m
|
  &@E@p m
)

@script:python@
E << rule12.E;
p << rule12.p;
@@

print(f"Rule12:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule13@
position p;
expression e;
expression E;
identifier m = {m_rule11.m};
binary operator b = {-, /, %, &&, ||, >, >=, <, <=, ==};
@@

(
  e b@E@p m
|
  !@E@p m
|
  +@E@p m
|
  -@E@p m
)

@script:python@
E << rule13.E;
p << rule13.p;
@@

print(f"Rule13:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule14@
position p;
expression E;
identifier m = {m_rule1.m, m_rule2.m, m_rule4.m, m_rule5.m, m_rule9.m, m_rule10.m, m_rule11.m};
@@

(
  ~@E@p m
)

@script:python@
E << rule14.E;
p << rule14.p;
@@

print(f"Rule14:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")

@rule15@
position p;
expression e;
expression E;
identifier m1 = {m_rule3.m, m_rule6.m, m_rule7.m, m_rule8.m};
identifier m2 = {m_rule11.m};
binary operator b = {&, |, ^, <<, >>};
@@

(
  +@E@p m1
|
  -@E@p m1
|
  !@E@p m1
|
  ~@E@p m1
|
  e b@E@p m2
)

@script:python@
E << rule15.E;
p << rule15.p;
@@

print(f"Rule14:")
print(f"    line: {p[0].line}")
print(f"    E: {E}")