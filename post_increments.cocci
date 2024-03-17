@post_increment@
expression e;
position p;
@@

e@p++

@script:python@
p << post_increment.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")
