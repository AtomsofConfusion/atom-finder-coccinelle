@rule1@
position p;
type t1, t2;
identifier i1, i2;
expression e1, e2;
declaration d;
@@

(
  t1 i1 = e1;
  ...
  t2 i2 =@d@p i1;
)

@script:python@
p << rule1.p;
d << rule1.d;
t1 << rule1.t1;
t2 << rule1.t2;
@@

if t1 != t2:
  print(f"Rule1:")
  print(f"  line: {p[0].line}")
  print(f"  d: {d}")

@rule2@
position p;
type t1, t2;
identifier i1, i2;
expression e1, e2;
declaration d;
@@

(
  t1 i1 = e1;
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
  print(f"Rule2:")
  print(f"  line: {p[0].line}")
  print(f"  d: {d}")

@rule3a@
position p;
type t1, t2;
identifier i1, i2;
binary operator b != {<<, >>};
expression e1, e2, E;
@@

(
  t1 i1 = e1;
  t2 i2 = e2;
  ...
  i1 b@E@p i2
)

@script:python@
p << rule3a.p;
E << rule3a.E;
t1 << rule3a.t1;
t2 << rule3a.t2;
@@

if t1 != t2:
  print(f"Rule3:")
  print(f"  line: {p[0].line}")
  print(f"  E: {E}")

@rule3b@
position p;
type t1, t2;
identifier i1, i2;
assignment operator a != {<<=, >>=};
expression e1, e2, E;
@@

(
  t1 i1 = e1;
  t2 i2 = e2;
  ...
  i1 a@E@p i2
)

@script:python@
p << rule3b.p;
E << rule3b.E;
t1 << rule3b.t1;
t2 << rule3b.t2;
@@

if t1 != t2:
  print(f"Rule3:")
  print(f"  line: {p[0].line}")
  print(f"  E: {E}")

@f_rule4@
identifier fun, a;
type tf, ta;
@@

tf fun(ta a) {
  ...
}

@rule4@
position p;
type t != f_rule4.ta;
identifier a, fun = f_rule4.fun;
expression e, E;
@@

(
  t a = e;
  ...
  fun(a)@E@p
)

@script:python@
p << rule4.p;
E << rule4.E;
@@

print(f"Rule4:")
print(f"  line: {p[0].line}")
print(f"  E: {E}")


@rule5@
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
p << rule5.p;
S << rule5.S;
@@

print(f"Rule5:")
print(f"  line: {p[0].line}")
print(f"  S: {S}")

@rule6@
position p;
type t1, t2, t3;
identifier fun, i1, i2;
expression e;
statement S;
@@

t1 fun(t2 i1, t3 i2) {
  i1 = i2;
  ...
}

@script:python@
p << rule6.p;
S << rule6.S;
@@

if t2 != t3
  print(f"Rule6:")
  print(f"  line: {p[0].line}")
  print(f"  S: {S}")

@rule7@
position p;
constant c =~ "[+-]?[0-9]*\.[0-9]*";
identifier i;
type t != {double};
declaration d;
@@

t i =@d@p c;

@script:python@
p << rule7.p;
d << rule7.d;
@@

print(f"Rule7:")
print(f"  line: {p[0].line}")
print(f"  d: {d}")