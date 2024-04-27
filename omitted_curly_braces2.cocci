@rule1 disable braces0, neg_if@
position p;
statement S;
@@

//the single "else if" without curly braces between "if" and "else" will be matched
(
  if (...) {...}
  else if (...) {...}
  else {...}
|
  if (...) {...}
  else if (...)@p S
  else {...}
)

@script:python@
p << rule1.p;
@@

print(f"Rule1: Line {p[0].line} in file {p[0].file}")


@rule2 disable braces4, neg_if@
position p;
statement S;
@@

// match the "if" statement in a simple "if - else if - else" structure
(
  if (...) {
    S
  } else {
    ...
    if (...) {...} else {...}
    ...
  }
|
  if (...)@p
    S
  else {
    ...
    if (...) {...} else {...}
    ...
  }
)

@script:python@
p << rule2.p;
@@

print(f"Rule2: Line {p[0].line} in file {p[0].file}")