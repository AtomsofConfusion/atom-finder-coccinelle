@rule0@
expression e1, e2;
expression E;
position p;
binary operator bop;
@@

(
    e1 >@E@p e2
|
    e1 <@E@p e2
|
    e1 >=@E@p e2
|
    e1 <=@E@p e2
|
    e1 ==@E@p e2
|
    e1 !=@E@p e2
|
    e1 ||@E@p e2
|
    e1 &&@E@p e2
)


@script:python@
p << rule0.p;
e << rule0.E;
@@
print(e)
print(p)
print(f"Rule0: Line {p[0].line} in file {p[0].file}")

@rule1@
expression e;
statement s1, s2;
position p != rule0.p;
binary operator b;
@@

if (e@p) s1 else s2

@script:python@
p << rule1.p;
e << rule1.e;
@@

print(f"Rule1: Line {p[0].line} in file {p[0].file}")

@rule2@
expression e;
position p != rule0.p;
@@

(
while (e@p) {...}
|
do {...} while (e@p);
|
for (...;e@p;...) {...}
)

@script:python@
p << rule2.p;
e << rule2.e;
@@

print(f"Rule2: Line {p[0].line} in file {p[0].file}")

@rule3@
expression e, ec, el, er;
position p != rule0.p;
@@

ec@p ? el : er //cannot have semicolon here

@script:python@
p << rule3.p;
ec << rule3.ec;
@@

print(f"Rule3: Line {p[0].line} in file {p[0].file}")