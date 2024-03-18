
@omitted_braces@
expression e, x;
position p;
type t;
identifier i;
@@

(
if(...) @p
e;
|
while(...) @p
e;
|
for(t i = x;...;...) @p
e;
)

@script:python@
p << omitted_braces.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")