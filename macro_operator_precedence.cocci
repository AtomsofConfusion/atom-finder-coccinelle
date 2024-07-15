@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "operator-precedence"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    print(f"{ATOM_NAME},{file_path},{position[0].line},{position[0].column},\"{exp}\"")

def print_if_not_contained(exp, position, rule_name=""):
    start_line, start_col = int(position[0].line), int(position[0].column)
    end_line, end_col = int(position[0].line_end), int(position[0].column_end)
    new_range = {'start_line': start_line, 'start_col': start_col, 'end_line': end_line, 'end_col': end_col}
    if start_line in processed:
        subset = any(is_same_range(new_range, existing) for existing in processed[start_line])
        if not subset:
            processed[start_line].append(new_range)
            print_expression_and_position(exp, position, rule_name)
    else:
        processed[start_line] = [new_range]
        print_expression_and_position(exp, position, rule_name)

def is_same_range(current, previous):
    # Check if the current range is entirely within the previous range
    if (current['start_line'] == previous['start_line'] and current['start_col'] == previous['start_col']) and \
       (current['end_line'] == previous['end_line'] and current['end_col'] == previous['end_col']):
        return True
    return False


@m_rule1@
expression e1, e2;
identifier m;
binary operator b = {*, /, %};
@@

#define m e1 b e2

@m_rule2@
expression e1, e2;
identifier m;
binary operator b = {+, -};
@@

#define m e1 b e2

@m_rule3@
expression e1, e2;
identifier m;
binary operator b = {<<, >>};
@@

#define m e1 b e2

@m_rule4@
expression e1, e2;
identifier m;
binary operator b = {<, <=, >, >=};
@@

#define m e1 b e2

@m_rule5@
expression e1, e2;
identifier m;
binary operator b = {==, !=};
@@

#define m e1 b e2

@m_rule6@
expression e1, e2;
identifier m;
binary operator b = {&};
@@

#define m e1 b e2

@m_rule7@
expression e1, e2;
identifier m;
binary operator b = {^};
@@

#define m e1 b e2

@m_rule8@
expression e1, e2;
identifier m;
binary operator b = {|};
@@

#define m e1 b e2

@m_rule9@
expression e1, e2;
identifier m;
binary operator b = {&&};
@@

#define m e1 b e2

@m_rule10@
expression e1, e2;
identifier m;
binary operator b = {||};
@@

#define m e1 b e2

@m_rule11@
expression e1, e2, e3;
identifier m;
@@

#define m e1 ? e2 : e3

@rule1@
position p;
expression e;
expression E;
identifier m = {m_rule10.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=, &, ^, |, &&};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule1.E;
p << rule1.p;
@@

print_if_not_contained(E, p, "Rule1")

@rule2@
position p;
expression e;
expression E;
identifier m = {m_rule9.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=, &, ^, |};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule2.E;
p << rule2.p;
@@

print_if_not_contained(E, p, "Rule2")
@rule3@
position p;
expression e;
expression E;
identifier m = {m_rule8.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=, &, ^};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule3.E;
p << rule3.p;
@@

print_if_not_contained(E, p, "Rule3")

@rule4@
position p;
expression e;
expression E;
identifier m = {m_rule7.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=, &};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule4.E;
p << rule4.p;
@@

print_if_not_contained(E, p, "Rule4")

@rule5@
position p;
expression e;
expression E;
identifier m = {m_rule6.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=, ==, !=};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule5.E;
p << rule5.p;
@@

print_if_not_contained(E, p, "Rule5")

@rule6@
position p;
expression e;
expression E;
identifier m = {m_rule5.m};
binary operator b = {*, /, %, +, -, <<, >>, <, <=, >, >=};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule6.E;
p << rule6.p;
@@

print_if_not_contained(E, p, "Rule6")

@rule7@
position p;
expression e;
expression E;
identifier m = {m_rule4.m};
binary operator b = {*, /, %, +, -, <<, >>};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule7.E;
p << rule7.p;
@@

print_if_not_contained(E, p, "Rule7")

@rule8@
position p;
expression e;
expression E;
identifier m = {m_rule3.m};
binary operator b = {*, /, %, +, -};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule8.E;
p << rule8.p;
@@

print_if_not_contained(E, p, "Rule8")

@rule9@
position p;
expression e;
expression E;
identifier m = {m_rule2.m};
binary operator b = {*, /, %};
@@

(
  m b@E@p e
|
  e b@E@p m
)

@script:python@
E << rule9.E;
p << rule9.p;
@@

print_if_not_contained(E, p, "Rule9")

@rule10@
position p;
expression e;
expression E;
identifier m = {m_rule1.m, m_rule2.m, m_rule6.m, m_rule9.m, m_rule10.m};
@@

(
  +@E@p m
|
  -@E@p m
)

@script:python@
E << rule10.E;
p << rule10.p;
@@

print_if_not_contained(E, p, "Rule10")

@rule11@
position p;
expression e;
expression E;
identifier m = {m_rule1.m, m_rule2.m, m_rule9.m, m_rule10.m, rule4.m, rule5.m};
@@

(
  !@E@p m
)

@script:python@
E << rule11.E;
p << rule11.p;
@@

print_if_not_contained(E, p, "Rule11")
@rule12@
position p;
expression e;
expression E;
identifier m = {m_rule2.m};
@@

(
  *@E@p m
|
  &@E@p m
)

@script:python@
E << rule12.E;
p << rule12.p;
@@

print_if_not_contained(E, p, "Rule12")
@rule13@
position p;
expression e;
expression E;
identifier m = {m_rule11.m};
binary operator b = {-, /, %, &&, ||, >, >=, <, <=, ==};
@@

(
  e b@E@p m
|
  !@E@p m
|
  +@E@p m
|
  -@E@p m
)

@script:python@
E << rule13.E;
p << rule13.p;
@@

print_if_not_contained(E, p, "Rule13")

@rule14@
position p;
expression E;
identifier m = {m_rule1.m, m_rule2.m, m_rule4.m, m_rule5.m, m_rule9.m, m_rule10.m, m_rule11.m};
@@

(
  ~@E@p m
)

@script:python@
E << rule14.E;
p << rule14.p;
@@

print_if_not_contained(E, p, "Rule14")

@rule15@
position p;
expression e;
expression E;
identifier m1 = {m_rule3.m, m_rule6.m, m_rule7.m, m_rule8.m};
identifier m2 = {m_rule11.m};
binary operator b = {&, |, ^, <<, >>};
@@

(
  +@E@p m1
|
  -@E@p m1
|
  !@E@p m1
|
  ~@E@p m1
|
  e b@E@p m2
)

@script:python@
E << rule15.E;
p << rule15.p;
@@

print_if_not_contained(E, p, "Rule15")