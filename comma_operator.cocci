@script:python@
@@
processed = {}

@rule1@
expression e1, e2;
expression E;
position p;
@@

e1 ,@E@p e2

@script:python@
p << rule1.p;
E << rule1.E;
@@

line_number = p[0].line
new_range = {'start': p[0].column, 'end': p[0].column_end}

if line_number in processed:
  # Check if the new range is a subset of any of the existing ranges
  subset = any(is_subset(new_range, existing) for existing in processed[line_number])
  if not subset:
      # Add the new range if it is not a subset of existing ranges
      processed[line_number].append(new_range)
      # Ensure no existing range is a subset of the new one
      processed[line_number] = [existing for existing in processed[line_number] if not is_subset(existing, new_range)]
      print(f"Rule1: Line {p[0].line} in file {p[0].file}")
else:
  # Initialize the list with the new range if this is the first range for this line
  processed[line_number] = [new_range]
  print(f"Rule1: Line {p[0].line} in file {p[0].file}")

def is_subset(current, previous):
  # Check if the current range is a subset of the previous range
  return current['start'] >= previous['start'] and current['end'] <= previous['end']
  