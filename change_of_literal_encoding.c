@r@
expression E;
constant c;
position p;
type t;
identifier x;
statement S;
@@

c@p

@script:python@
p << r.p;
c << r.c;
@@

import re

def is_non_decimal(n):
    # Check if the string representation of the number is octal or hexadecimal
    return n!= "0" and re.match(r'^0[0-7]*$', n) or re.match(r'^0[xX][0-9a-fA-F]+$', n)

if is_non_decimal(c):
    for i in range(0, len(p)):
        print(f"Non-decimal numeric constant {c} at {p[i].file}:{p[i].line}")