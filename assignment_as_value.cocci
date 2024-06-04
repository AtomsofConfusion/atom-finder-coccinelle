@script:python@
@@
processed = {}

def is_subset(current, previous):
  # Check if the current range is a subset of the previous range
  return current['start'] >= previous['start'] and current['end'] <= previous['end']

@rule1@
expression e1, e2;
position p;
identifier i;
assignment operator aop;
declaration d;
type t;
@@

(
t@d@p i = e1 aop e2;
|
t@d@p i = (e1 aop e2);
)


@script:python@
p << rule1.p;
d << rule1.d;
@@

line_number = p[0].line
new_range = {'start': int(p[0].column), 'end': int(p[0].column_end)}
processed[line_number] = [new_range]
print(f"Rule1: Line {p[0].line} in file {p[0].file} - {p[0].column} - {p[0].column_end}")
print(f"                {d}")

@rule2@
expression e1, e2, e3, e4;
assignment operator aop1, aop2;
binary operator bop;
expression E;
position p;
@@

(
e1 aop1@E@p e2 = e3
|
e1 aop1@E@p e2 += e3
|
e1 aop1@E@p e2 -= e3
|
e1 aop1@E@p e2 *= e3
|
e1 aop1@E@p e2 /= e3
|
e1 aop1@E@p e2 |= e3
|
e1 aop1@E@p e2 &= e3
|
e1 aop1@E@p (e2 aop2 e3)
|
e1 aop1@E@p e2 bop (e3 aop2 e4)
)


@script:python@
p << rule2.p;
E << rule2.E;
@@

line_number = p[0].line
new_range = {'start': int(p[0].column), 'end': int(p[0].column_end)}

if line_number in processed:
  # Check if the new range is a subset of any of the existing ranges
  subset = any(is_subset(new_range, existing) for existing in processed[line_number])
  if not subset:
      # Add the new range if it is not a subset of existing ranges
      processed[line_number].append(new_range)
      # Ensure no existing range is a subset of the new one
      processed[line_number] = [existing for existing in processed[line_number] if not is_subset(existing, new_range)]
      print(f"Rule2: Line {p[0].line} in file {p[0].file} - {p[0].column} - {p[0].column_end}")
      print(f"              {E}")
else:
  # Initialize the list with the new range if this is the first range for this line
  processed[line_number] = [new_range]
  print(f"Rule2: Line {p[0].line} in file {p[0].file} - {p[0].column} - {p[0].column_end}")
  print(f"              {E}")

@rule3@
expression e1, e2;
position p;
declaration d;
assignment operator aop;
identifier i;
type t;
statement s;
@@

(
for (t@d@p i = e1 aop e2;...;...) s
|
for (t@d@p i = (e1 aop e2);...;...) s
)

@script:python@
d << rule3.d;
p << rule3.p;
@@

print(f"Rule3: Line {p[0].line} in file {p[0].file} - {p[0].column} - {p[0].column_end}")
print(f"                {d}")

@rule4@
expression e1, e2;
expression E;
assignment operator aop;
statement s;
position p;
@@

(
while (<+... e1 aop@E@p e2 ...+>) s
|
for (...;<+... e1 aop@E@p e2 ...+>;...) s
|
for (...;...;<+... e1 aop@E@p e2 ...+>) s
)

@script:python@
p << rule4.p;
E << rule4.E;
@@

line_number = p[0].line
new_range = {'start': int(p[0].column), 'end': int(p[0].column_end)}

if line_number in processed:
  subset = any(is_subset(new_range, existing) for existing in processed[line_number])
  if not subset:
      # Add the new range if it is not a subset of existing ranges
      processed[line_number].append(new_range)
      # Ensure no existing range is a subset of the new one
      processed[line_number] = [existing for existing in processed[line_number] if not is_subset(existing, new_range)]
      print(f"Rule4: Line {p[0].line} in file {p[0].file} - {p[0].column} - {p[0].column_end}")
      print(f"              {E}")
else:
  processed[line_number] = [new_range]
  print(f"Rule4: Line {p[0].line} in file {p[0].file} - {p[0].column} - {p[0].column_end}")
  print(f"              {E}")

@rule5@
expression e1, e2;
expression E;
assignment operator aop;
statement s1, s2;
position p;
@@

if (<+... e1 aop@E@p e2 ...+>) s1 else s2

@script:python@
E << rule5.E;
p << rule5.p;
@@

print(f"Rule5: Line {p[0].line} in file {p[0].file} - {p[0].column} - {p[0].column_end}")
print(f"                {E}")