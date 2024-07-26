@rule1@
position p;
type tf, ti;
identifier fun, i;
assignment operator a;
expression e;
expression E;
@@

(
  tf fun(..., ti i, ...) {
    <+...
    i a@E@p e
    ...+>
  }
|
  tf fun(..., ti i, ...) {
    <+...
    i++@E@p
    ...+>
  }
|
  tf fun(..., ti i, ...) {
    <+...
    i--@E@p
    ...+>
  }
)


@script:python@
p << rule1.p;
E << rule1.E;
@@

print(f"Rule1: ")
print(f"  line: {p[0].line}")
print(f"  E: {E}")