@test disable neg_if@ 
expression e;
position p, p1, p2;
constant c;
identifier i, i1, i2;
statement s;
@@ 

(
  if (i1 == i2)@p {
    printf(...);
  } else {
    e;
  }
)


@script:python@
p << test.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")