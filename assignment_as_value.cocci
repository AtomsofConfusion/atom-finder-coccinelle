@script:python@
@@
processed = {}

def is_subset(current, previous):
  # Check if the current range is a subset of the previous range
  return current['start'] >= previous['start'] and current['end'] <= previous['end']

@rule1@
expression e1, e2, e3;
assignment operator aop1, aop2;
expression E;
position p;
@@

(
e1 aop1@E@p (e2 aop2 e3)
)


@script:python@
p << rule1.p;
E << rule1.E;
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
      print(f"Rule1: Line {p[0].line} in file {p[0].file} - {p[0].column} - {p[0].column_end}")
      print(f"              {E}")
else:
  # Initialize the list with the new range if this is the first range for this line
  processed[line_number] = [new_range]
  print(f"Rule1: Line {p[0].line} in file {p[0].file} - {p[0].column} - {p[0].column_end}")
  print(f"              {E}")


@rule2@
expression e1, e2;
position p1, p2;
identifier i;
assignment operator aop;
type t;
@@

(
t@p1 i = e1 aop e2@p2;
|
t@p1 i = (e1 aop e2@p2);
)


@script:python@
p1 << rule2.p1;
p2 << rule2.p2;
e1 << rule2.e1;
e2 << rule2.e2;
t << rule2.t;
i << rule2.i;
aop << rule2.aop;
@@

print(f"Rule2: Line {p1[0].line} in file {p1[0].file} - {p1[0].column} - {p2[0].column_end}")
print(f"                {t} {i} = {e1} {aop} {e2}")

@rule3@
expression e1, e2;
position p1, p2;
identifier i;
type t;
statement s;
@@

(
for (t@p1 i = e1 = e2@p2;...;...) s
|
for (t@p1 i = e1 += e2@p2;...;...) s
|
for (t@p1 i = e1 -= e2@p2;...;...) s
|
for (t@p1 i = e1 *= e2@p2;...;...) s
|
for (t@p1 i = e1 /= e2@p2;...;...) s
|
for (t@p1 i = e1 |= e2@p2;...;...) s
|
for (t@p1 i = e1 &= e2@p2;...;...) s
)

@script:python@
p1 << rule3.p1;
p2 << rule3.p2;
e1 << rule3.e1;
e2 << rule3.e2;
t << rule3.t;
i << rule3.i;
@@

print(f"Rule3: Line {p1[0].line} in file {p1[0].file} - {p1[0].column} - {p2[0].column_end}")
print(f"                {t} {i} = {e1} = {e2}")

@rule4@
expression e1, e2;
identifier i;
type t;
assignment operator aop;
position p1, p2;
@@

(
t i = (e1@p1 aop e2@p2);
)

@script:python@
p1 << rule4.p1;
p2 << rule4.p2;
t << rule4.t;
i << rule4.i;
e1 << rule4.e1;

@@

print(f"Rule4: Line {p1[0].line} in file {p1[0].file} - {p1[0].column} - {p2[0].column_end}")
//print(f"                {t} {i} = {e1} = {e2}")
