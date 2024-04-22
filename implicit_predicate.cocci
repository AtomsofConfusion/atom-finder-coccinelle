@r@
expression e, e1, e2, e3, e4;
constant c1, c2;
identifier v1, v2;
position p;
statement s;
@@

(
  if (e1 || e2) {...}
|
  if (e1 && e2) {...} // add constraints on matching
| 
  if (e@p) {...}
|
  if (e1) {...}
  else if (e2@p) {
    s
    ... when != e2 == ... //this part has no effect
        when != e2 != ...
        when != e2 || ...
        when != e2 && ...
  }
)

@script:python@
p << r.p;
e << r.e;
@@

if "==" not in e and "!=" not in e and ">=" not in e and "<=" not in e and ">" not in e and "<" not in e: // add constraints on Python "printf"
    print(f"Line {p[0].line} in file {p[0].file}")