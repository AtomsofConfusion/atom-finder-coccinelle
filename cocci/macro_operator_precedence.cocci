@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "operator-precedence"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col},\"{exp}\"")


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
@@

#define m e1 & e2

@m_rule7@
expression e1, e2;
identifier m;
@@

#define m e1 ^ e2

@m_rule8@
expression e1, e2;
identifier m;
@@

#define m e1 | e2

@m_rule9@
expression e1, e2;
identifier m;
@@

#define m e1 && e2

@m_rule10@
expression e1, e2;
identifier m;
@@

#define m e1 || e2

@m_rule11@
expression e1, e2, e3;
identifier m;
@@

#define m e1 ? e2 : e3

@m_rule12@
identifier m, x;
@@

(
  #define m(x) (<+... (-x) ...+>)
|
  #define m(x) (<+... (+x) ...+>)
|
  #define m(x) (<+... (!x) ...+>)
|
  #define m(x) (<+... (~x) ...+>)
)

@m_rule13@
identifier m, x;
expression e;
binary operator b = {*, /, %};
@@

(
  #define m(x) (<+... e b x ...+>)
|
  #define m(x) (<+... x b e ...+>)
)

@m_rule14@
identifier m, x;
expression e;
binary operator b = {+, -};
@@

(
  #define m(x) (<+... e b x ...+>)
|
  #define m(x) (<+... x b e ...+>)
)

@m_rule15@
identifier m, x;
expression e;
binary operator b = {<<, >>};
@@

(
  #define m(x) (<+... e b x ...+>)
|
  #define m(x) (<+... x b e ...+>)
)

@m_rule16@
identifier m, x;
expression e;
binary operator b = {<, <=, >, >=};
@@

(
  #define m(x) (<+... e b x ...+>)
|
  #define m(x) (<+... x b e ...+>)
)

@m_rule17@
identifier m, x;
expression e;
binary operator b = {==, !=};
@@

(
  #define m(x) (<+... e b x ...+>)
|
  #define m(x) (<+... x b e ...+>)
)

@m_rule18@
identifier m, x;
expression e;
@@

(
  #define m(x) (<+... e & x ...+>)
|
  #define m(x) (<+... x & e ...+>)
)

@m_rule19@
identifier m, x;
expression e;
@@

(
  #define m(x) (<+... e ^ x ...+>)
|
  #define m(x) (<+... x ^ e ...+>)
)

@m_rule20@
identifier m, x;
expression e;
@@

(
  #define m(x) (<+... e | x ...+>)
|
  #define m(x) (<+... x | e ...+>)
)

@m_rule21@
identifier m, x;
expression e;
@@

(
  #define m(x) (<+... e && x ...+>)
|
  #define m(x) (<+... x && e ...+>)
)

@m_rule22@
identifier m, x;
expression e;
@@

(
  #define m(x) (<+... e || x ...+>)
|
  #define m(x) (<+... x || e ...+>)
)

@m_rule23@
identifier m, x;
expression e;
binary operator b;
@@

(
  #define m(x) <+... e b x ...+>
|
  #define m(x) <+... x b e ...+>
)

@m_rule24@
identifier m, x;
@@

#define m(x) ...

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

print_expression_and_position(E, p, "Rule1")

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

print_expression_and_position(E, p, "Rule2")
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

print_expression_and_position(E, p, "Rule3")

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

print_expression_and_position(E, p, "Rule4")

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

print_expression_and_position(E, p, "Rule5")

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

print_expression_and_position(E, p, "Rule6")

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

print_expression_and_position(E, p, "Rule7")

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

print_expression_and_position(E, p, "Rule8")

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

print_expression_and_position(E, p, "Rule9")

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

print_expression_and_position(E, p, "Rule10")

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

print_expression_and_position(E, p, "Rule11")
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

print_expression_and_position(E, p, "Rule12")
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

print_expression_and_position(E, p, "Rule13")

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

print_expression_and_position(E, p, "Rule14")

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

print_expression_and_position(E, p, "Rule15")

@rule16@
position p;
identifier m = {m_rule12.m};
expression e1, e2;
binary operator b;
expression E;
@@

m(e1 b e2) @E@p

@script:python@
E << rule16.E;
p << rule16.p;
@@

print_expression_and_position(E, p, "Rule16")

@rule17@
position p;
identifier m = {m_rule13.m};
binary operator b = {+, -, <<, >>, <, <=, >, >=, ==, !=, &, ^, |, &&, ||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule17.E;
p << rule17.p;
@@

print_expression_and_position(E, p, "Rule17")

@rule18@
position p;
identifier m = {m_rule14.m};
binary operator b = {<<, >>, <, <=, >, >=, ==, !=, &, ^, |, &&, ||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule18.E;
p << rule18.p;
@@

print_expression_and_position(E, p, "Rule18")

@rule19@
position p;
identifier m = {m_rule15.m};
binary operator b = {<, <=, >, >=, ==, !=, &, ^, |, &&, ||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule19.E;
p << rule19.p;
@@

print_expression_and_position(E, p, "Rule19")

@rule20@
position p;
identifier m = {m_rule16.m};
binary operator b = {==, !=, &, ^, |, &&, ||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule20.E;
p << rule20.p;
@@

print_expression_and_position(E, p, "Rule20")

@rule21@
position p;
identifier m = {m_rule17.m};
binary operator b = {&, ^, |, &&, ||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule21.E;
p << rule21.p;
@@

print_expression_and_position(E, p, "Rule21")

@rule22@
position p;
identifier m = {m_rule18.m};
binary operator b = {^, |, &&, ||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule22.E;
p << rule22.p;
@@

print_expression_and_position(E, p, "Rule22")

@rule23@
position p;
identifier m = {m_rule19.m};
binary operator b = {^, |, &&, ||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule23.E;
p << rule23.p;
@@

print_expression_and_position(E, p, "Rule23")

@rule24@
position p;
identifier m = {m_rule20.m};
binary operator b = {|, &&, ||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule24.E;
p << rule24.p;
@@

print_expression_and_position(E, p, "Rule24")

@rule25@
position p;
identifier m = {m_rule21.m};
binary operator b = {&&, ||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule25.E;
p << rule25.p;
@@

print_expression_and_position(E, p, "Rule17")

@rule26@
position p;
identifier m = {m_rule22.m};
binary operator b = {||};
expression e1, e2;
expression E;
@@

(
  m(e1 b e2) @E@p
)

@script:python@
E << rule26.E;
p << rule26.p;
@@

print_expression_and_position(E, p, "Rule26")

@rule27@
position p;
identifier m = {m_rule23.m};
expression e1, e2, e3;
expression E;
@@

(
  m(e1 ? e2 : e3) @E@p
)

@script:python@
E << rule27.E;
p << rule27.p;
@@

print_expression_and_position(E, p, "Rule27")

@rule28@
position p;
identifier m = {m_rule24.m}, x;
expression E;
@@

(
  m(x++) @E@p
|
  m(x--) @E@p
|
  m(++x) @E@p
|
  m(--x) @E@p
)

@script:python@
E << rule28.E;
p << rule28.p;
@@

print_expression_and_position(E, p, "Rule28")