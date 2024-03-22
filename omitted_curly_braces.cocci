
@omitted_braces@
expression e, x, e1, e2;
position p;
type t;
identifier i;
statement S;
@@

(
if(...) S
else @p
e;
|
if(...) @p
e;
else 
S
|
while(...) @p e;
|
for(t i = x;...;...) @p
e;
)

@script:python@
p << omitted_braces.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")