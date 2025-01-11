@script:python@
@@
from pathlib import Path
debug = False
ATOM_NAME = "type_conversion"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col},\"{exp}\"")


type_conversion_confusions = {
    "long long": ["int", "short", "char"],
    "unsigned long long": ["long long", "long", "int", "unsigned int", "short", "unsigned short"],
    "double": ["float", "int", "short", "char"],
    "float": ["int", "short", "char"],
    "unsigned int": ["int", "short", "char"],
    "long": ["int", "short", "char"],
    "int": ["short", "char", "unsigned int"],
    "enum": ["int", "short", "char"],
    "pointer": ["int", "char*"],  # Simplified for generality
}

@rule1@
position p;
type t1, t2;
identifier i1, i2;
expression e, e1, e2;
declaration d;
binary operator bop1, bop2;
@@

//  using t2 i2 =@d@p <+... i1 ...+>; leads to the patch timing out when running against large files
(
  t1 i1 = e;
  ...
  t2 i2 =@d@p i1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p e1 bop1 i1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p i1 bop1 e1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p e1 bop1 i1 bop2 e2;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p e2 bop1 i1 bop1 e1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p <+... i1++ ...+>;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p <+... i1-- ...+>;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p <+... --i1 ...+>;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p <+... ++i1 ...+>;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p e1 bop1 (t2) i1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p (t2) i1 bop1 e1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p e1 bop1 (t2) i1 bop2 e2;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p e2 bop1 (t2)  i1 bop1 e1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p (t2) i1;
)


@script:python@
p << rule1.p;
d << rule1.d;
t1 << rule1.t1;
t2 << rule1.t2;
@@

if t1 != t2:
  if t2 in type_conversion_confusions.get(t1, []):
    print_expression_and_position(d, p, "Rule 1")


@rule2@
position p;
type t1, t2;
identifier i1, i2;
expression e1, e2;
declaration d;
binary operator bop1, bop2;
@@


(
  t1 i1 = e;
  ...
  t2 i2 =@d@p e1 bop1 (t2) i1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p (t2) i1 bop1 e1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p e1 bop1 (t2) i1 bop2 e2;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p e2 bop1 (t2)  i1 bop1 e1;
|
  t1 i1 = e;
  ...
  t2 i2 =@d@p (t2) i1;
)

@script:python@
p << rule2.p;
d << rule2.d;
t1 << rule2.t1;
t2 << rule2.t2;
@@

if t1 != t2:
  if t2 in type_conversion_confusions.get(t1, []):
    print_expression_and_position(d, p, "Rule 2")



@rule3@
position p;
type t1, t2;
t1 i1;
t2 i2;
binary operator b != {<<, >>};
expression E;
@@

i1 b@E@p i2

@script:python@
p << rule3.p;
E << rule3.E;
t1 << rule3.t1;
t2 << rule3.t2;
@@

if t1 != t2:
  if t2 in type_conversion_confusions.get(t1, []) or t1 in type_conversion_confusions.get(t2, []):
    print_expression_and_position(E, p, "Rule 3")


@rule4@
position p;
type t1, t2;
t1 i1;
t2 i2;
assignment operator a != {<<=, >>=};
expression E;
@@

i1 a@E@p i2


// removing this for the sake of performance

/*
@script:python@
p << rule4.p;
E << rule4.E;
t1 << rule4.t1;
t2 << rule4.t2;
@@

if t1 != t2:
  if t1 in type_conversion_confusions.get(t2, []):
    print_expression_and_position(E, p, "Rule 4")

@f_rule5@
identifier fun, a;
type tf, ta;
@@

tf fun(..., ta a, ...) {
  ...
}


@rule5@
position p;
type t != f_rule5.ta;
identifier a, fun = f_rule5.fun;
expression e, E;
@@

(
  t a = e;
  ...
  fun(a)@E@p

)
// fun(..., a, ...)@E@p is also too slow

@script:python@
p << rule5.p;
E << rule5.E;
t1 << f_rule5.ta;
t2 << rule5.t;
@@

if t1 != t2:
  if t1 in type_conversion_confusions.get(t2, []):
    print_expression_and_position(E, p, "Rule 5")
*/

@rule6@
position p;
type t1, t2;
identifier fun, i1;
expression e;
statement S;
@@

t1 fun(...) {
  t2 i1 = e;
  ... 
  return i1; @S@p
}

@script:python@
p << rule6.p;
S << rule6.S;
t1 << rule6.t1;
t2 << rule6.t2;
@@

if t1 != t2:
  if t1 in type_conversion_confusions.get(t2, []):
    print_expression_and_position(S, p, "Rule 6")



@rule7@
position p;
constant c =~ "[+-]?[0-9]*\.[0-9]*";
identifier i;
type t != {float, double, long double};
declaration d;
@@

t i =@d@p c;

@script:python@
p << rule7.p;
d << rule7.d;
@@

print_expression_and_position(d, p, "Rule 7")

@rule8@
position p;
constant c =~ "[+-]?[0-9]*\.[0-9]*";
type t != {float, double, long double};
binary operator b;
assignment operator a;
expression e;
expression E;
@@

(
  e b@E@p (t) c
|
  (t) c b@E@p e
|
  e a@E@p (t) c
)

// this also detects lines without (t)


@script:python@
p << rule8.p;
E << rule8.E;
@@

print_expression_and_position(E, p, "Rule 8")

