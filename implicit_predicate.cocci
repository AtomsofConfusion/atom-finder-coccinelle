@rule1@
expression e;
statement s1, s2;
position p;
binary operator b;
@@

if (e@p) s1 else s2

@script:python@
p << rule1.p;
e << rule1.e;
@@

if "==" not in e and "!=" not in e and ">=" not in e and "<=" not in e and ">" not in e and "<" not in e and "||" not in e and "&&" not in e:
    print(f"Rule1: Line {p[0].line} in file {p[0].file}")

@rule2@
expression e;
position p;
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

if "==" not in e and "!=" not in e and ">=" not in e and "<=" not in e and ">" not in e and "<" not in e and "||" not in e and "&&" not in e:
    print(f"Rule2: Line {p[0].line} in file {p[0].file}")

@rule3@
expression e, ec, el, er;
position p;
@@

ec@p ? el : er //cannot have semicolon here

@script:python@
p << rule3.p;
ec << rule3.ec;
@@

if "==" not in ec and "!=" not in ec and ">=" not in ec and "<=" not in ec and ">" not in ec and "<" not in ec and "||" not in ec and "&&" not in ec:
    print(f"Rule3: Line {p[0].line} in file {p[0].file}")