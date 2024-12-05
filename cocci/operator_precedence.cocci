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

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col}\"{exp}\"")


@rule1@
position p;
binary operator b1 = {*, /, %};
expression e, e1, e2;
expression E;
@@

(
e1 b1 e +@E@p e2
|
e1 b1 e -@E@p e2
)

@script:python@
E << rule1.E;
p << rule1.p;
@@

print_expression_and_position(E, p, "Rule1")

@rule2@
position p;
binary operator b1 = {*, /, %, +, -};
expression e, e1, e2;
expression E;
@@

(
e1 b1 e >>@E@p e2
|
e1 b1 e <<@E@p e2
)

@script:python@
E << rule2.E;
p << rule2.p;
@@

print_expression_and_position(E, p, "Rule2")


@rule3@
position p;
// binary operator b1 = {*, /, %, +, -, >>, <<};
binary operator b1 = {>>, <<};
expression e, e1, e2;
expression E;
@@

(
e1 b1 e >@E@p e2
|
e1 b1 e >=@E@p e2
|
e1 b1 e <@E@p e2
|
e1 b1 e <=@E@p e2
)

@script:python@
E << rule3.E;
p << rule3.p;
@@

print_expression_and_position(E, p, "Rule3")

@rule4@
position p;
// binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=};
binary operator b1 = {>>, <<};
expression e, e1, e2;
expression E;
@@

(
e1 b1 e ==@E@p e2
|
e1 b1 e !=@E@p e2
)

@script:python@
E << rule4.E;
p << rule4.p;
@@

print_expression_and_position(E, p, "Rule4")

@rule5@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, ==, !=};
expression e, e1, e2;
expression E;
@@

e1 b1 e &@E@p e2

@script:python@
E << rule5.E;
p << rule5.p;
@@

print_expression_and_position(E, p, "Rule5")

@rule6@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, ==, !=, &};
expression e, e1, e2;
expression E;
@@

e1 b1 e ^@E@p e2

@script:python@
E << rule6.E;
p << rule6.p;
@@

print_expression_and_position(E, p, "Rule6")


@rule7@
position p;
binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, ==, !=, &, ^};
expression e, e1, e2;
expression E;
@@

e1 b1 e |@E@p e2

@script:python@
E << rule7.E;
p << rule7.p;
@@

print_expression_and_position(E, p, "Rule7")

@rule8@
position p;
// binary operator b1 = {*, /, %, +, -, >>, <<, <, >=, <=, ==, !=, &, ^, |};
binary operator b1 = {*, /, %, +, -, >>, <<, &, ^, |};
expression e, e1, e2;
expression E;
@@

e1 b1 e &&@E@p e2

@script:python@
E << rule8.E;
p << rule8.p;
@@

print_expression_and_position(E, p, "Rule8")


@rule9@
position p;
// binary operator b1 = {*, /, %, +, -, >>, <<, <, >=, <=, ==, !=, &, ^, |, &&};
binary operator b1 = {*, /, %, +, -, >>, <<, &, ^, |, &&};
expression e, e1, e2;
expression E;
@@

e1 b1 e ||@E@p e2

@script:python@
E << rule9.E;
p << rule9.p;
@@

print_expression_and_position(E, p, "Rule9")


@rule10@
position p;
// binary operator b1 = {*, /, %, +, -, >>, <<, >, <, >=, <=, ==, !=, &, ^, |, &&, ||};
binary operator b1 = {*, /, %, +, -, >>, <<, &, ^, |, &&, ||}; 
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

print_expression_and_position(E, p, "Rule10")

@rule11@
position p;
// binary operator b = {+, -, >>, <<, >, <, >=, <=, ==, !=, &, ^, |, &&, ||} ;
binary operator b = {+, -, >>, <<, &, ^, |, &&, ||} ;
expression e1, e2, e3;
expression E;
@@

(
e1 b@E@p e2 * e3
|
e1 b@E@p e2 / e3
|
e1 b@E@p e2 % e3
)

@script:python@
E << rule11.E;
p << rule11.p;
@@
print_expression_and_position(E, p, "Rule11")


@rule12@
position p;
// binary operator b = {>>, <<, >, <, >=, <=, ==, !=, &, ^, |, &&, ||} ;
binary operator b = {>>, <<, &, ^, |, &&, ||} ;
expression e1, e2, e3;
expression E;
@@

(
e1 b@E@p e2 + e3
|
e1 b@E@p e2 - e3
)

@script:python@
E << rule12.E;
p << rule12.p;
@@
print_expression_and_position(E, p, "Rule12")

@rule13@
position p;
binary operator b = {>, <, >=, <=, ==, !=, &, ^, |, &&, ||} ;
expression e1, e2, e3;
expression E;
@@

(
e1 b@E@p e2 >> e3
|
e1 b@E@p e2 << e3
)

@script:python@
E << rule13.E;
p << rule13.p;
@@
print_expression_and_position(E, p, "Rule13")

@rule14@
position p;
// binary operator b = {==, !=, &, ^, |, &&, ||} ;
binary operator b = {&, ^, |} ;
expression e1, e2, e3;
expression E;
@@

(
e1 b@E@p e2 < e3
|
e1 b@E@p e2 > e3
|
e1 b@E@p e2 <= e3
|
e1 b@E@p e2 >= e3
)

@script:python@
E << rule14.E;
p << rule14.p;
@@
print_expression_and_position(E, p, "Rule14")


@rule15@
position p;
// binary operator b = {&, ^, |, &&, ||} ;
binary operator b = {&, ^, |} ;
expression e1, e2, e3;
expression E;
@@

(
e1 b@E@p e2 == e3
|
e1 b@E@p e2 != e3
)

@script:python@
E << rule15.E;
p << rule15.p;
@@
print_expression_and_position(E, p, "Rule15")


@rule16@
position p;
//binary operator b = {^, |, &&, ||} ;
expression e1, e2, e3;
expression E;
@@

(
  e1 ^@E@p e2 & e3
|
  e1 |@E@p e2 & e3
|
  e1 &&@E@p e2 & e3
|
  e1 ||@E@p e2 & e3
)

@script:python@
E << rule16.E;
p << rule16.p;
@@
print_expression_and_position(E, p, "Rule16")

@rule17@
position p;
//binary operator b = {|, &&, ||} ;
expression e1, e2, e3;
expression E;
@@

(
  e1 |@E@p e2 ^ e3
|
  e1 &&@E@p e2 ^ e3
|
  e1 ||@E@p e2 ^ e3
)

@script:python@
E << rule17.E;
p << rule17.p;
@@
print_expression_and_position(E, p, "rule17")

@rule18@
position p;
binary operator b = {&&, ||} ;
expression e1, e2, e3;
expression E;
@@

(
  e1 &&@E@p e2 | e3
|
  e1 ||@E@p e2 | e3
)

@script:python@
E << rule18.E;
p << rule18.p;
@@
print_expression_and_position(E, p, "rule18")

@rule19@
position p;
expression e1, e2, e3;
expression E;
@@

(
  e1 ||@E@p e2 && e3
|
  e1 ||@E@p e2 + e3
|
  e1 ||@E@p e2 - e3
|
  e1 ||@E@p e2 << e3
|
  e1 ||@E@p e2 >> e3
|
  e1 &&@E@p e2 + e3
|
  e1 &&@E@p e2 - e3
|
  e1 &&@E@p e2 << e3
|
  e1 &&@E@p e2 >> e3
)

@script:python@
E << rule19.E;
p << rule19.p;
@@
print_expression_and_position(E, p, "rule19")

@rule20@
position p;
expression e1, e2, e3;
binary operator b1 = {+, -, *, /, &, &&, ||};
expression E;
@@

(
  +e1 b1@E@p e2
|
  -e1 b1@E@p e2
)

@script:python@
E << rule20.E;
p << rule20.p;
@@

print_expression_and_position(E, p, "rule20")

@rule21@
position p;
expression e1, e2, e3;
binary operator b1 = {+, -, *, /, %, &&, ||, >, >=, <, <=, ==};
expression E;
@@

(
  !e1 b1@E@p e2
)
@script:python@
E << rule21.E;
p << rule21.p;
@@

print_expression_and_position(E, p, "rule21")

@rule23@
position p;
expression e1, e2;
expression E;
@@

(
  *@E@p e1++
|
  *@E@p e1--
|
  *@E@p++e1
|
  *@E@p--e1
|
  *e1 +@E@p e2
|
  &@E@p e1++
|
  &@E@p e1--
|
  &@E@p++e1
|
  &@E@p--e1
|
  &e1 +@E@p e2
)
@script:python@
E << rule23.E;
p << rule23.p;
@@

print_expression_and_position(E, p, "Rule23")

@rule24@
position p;
expression e1, e2, e3, e4;
binary operator b1 = {-, /, %, &&, ||, >, >=, <, <=, ==};
expression E;
@@

(
  !e1 ?@E@p e2 : e3
|
  +e1 ?@E@p e2 : e3
|
  -e1 ?@E@p e2 : e3
|
  e1 b1 e2 ?@E@p e3 : e4
)
@script:python@
E << rule24.E;
p << rule24.p;
@@

print_expression_and_position(E, p, "Rule24")

@rule25@
position p;
expression e1, e2, e3, e4;
binary operator b1 = {+, -, *, /, %, &&, ||, >, >=, <, <=, ==};
identifier i1, i2;
expression E;
@@

(
  ~e1 b1@E@p e2
|
  ~@E@p e1++
|
  ~@E@p e1--
|
  ~@E@p++e1
|
  ~@E@p--e1
|
  ~@E@p i1.i2
|
  ~@E@p i1->i2 
|
  ~e1 ?@E@p e2 : e3
)

@script:python@
E << rule25.E;
p << rule25.p;
@@

print_expression_and_position(E, p, "Rule25")

@rule26@
position p;
expression e1, e2, e3, e4;
binary operator b1 = {&, |, ^, <<, >>};
expression E;
@@

(
  +e1 b1@E@p e2
|
  -e1 b1@E@p e2
|
  !e1 b1@E@p e2
|
  ~e1 b1@E@p e2
|
  e1 b1 e2 ?@E@p e3 : e4
)

@script:python@
E << rule26.E;
p << rule26.p;
@@

print_expression_and_position(E, p, "Rule26")