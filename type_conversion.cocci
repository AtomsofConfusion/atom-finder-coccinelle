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

@rule3@
position p;
type t1, t2;
identifier i1, i2;
binary operator b;
expression e1, e2, E;
declaration d;
@@

(
  t1 i1 = e1;
  t2 i2 = e2;
  ...
  i1 b@E@p i2
)

@script:python@
p << rule3.p;
E << rule3.E;
t1 << rule3.t1;
t2 << rule3.t2;
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
type t1;
type t2;
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