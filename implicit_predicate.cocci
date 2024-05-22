@rule01@
expression e1, e2;
expression E;
position p;
@@

e1 >@E@p e2

@rule02@
expression e1, e2;
expression E;
position p;
@@

e1 <@E@p e2

@rule03@
expression e1, e2;
expression E;
position p;
@@

e1 >=@E@p e2

@rule04@
expression e1, e2;
expression E;
position p;
@@

e1 <=@E@p e2

@rule05@
expression e1, e2;
expression E;
position p;
@@

e1 ==@E@p e2

@rule06@
expression e1, e2;
expression E;
position p;
@@

e1 !=@E@p e2

@rule1@
expression e;
statement s1, s2;
position p != {rule01.p, rule02.p, rule03.p, rule04.p, rule05.p, rule06.p};
@@

if (e@p) s1 else s2

@script:python@
p << rule1.p;
e << rule1.e;
@@

print(f"Rule1: Line {p[0].line} in file {p[0].file}")

@rule2@
expression e;
position p != {rule01.p, rule02.p, rule03.p, rule04.p, rule05.p, rule06.p};
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
position p != {rule01.p, rule02.p, rule03.p, rule04.p, rule05.p, rule06.p};
@@

ec@p ? el : er 

@script:python@
p << rule3.p;
ec << rule3.ec;
@@

print(f"Rule3: Line {p[0].line} in file {p[0].file}")