@test@
expression e;
position p;
constant c;
identifier i, i1;
@@ 

int i = c;
<...
i = ...;
...>
int i1@p = 2;

@script:python@
p << test.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")