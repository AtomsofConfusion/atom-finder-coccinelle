@r@
identifier fun, var;
expression e;
constant c;
position p;
type t;
@@

(
t fun(..., t var, ...) {
  ...
  var@p = e;
  ...
}
)

@script:python@
p << r.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")