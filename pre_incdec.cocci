@non_atoms@
expression e,x;
statement S;
type t;
identifier i;
position p;
@@

(
++e@p;
|
for(...;...;++e@p) S
|
for(t i = x;...;++e@p) S
|
--e@p;
|
for(...;...;--e@p) S
|
for(t i = x;...;--e@p) S
)

@pre_increment@
expression e;
position p != non_atoms.p;
@@

(
++e@p
|
--e@p
)

@script:python@
p << pre_increment.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")
