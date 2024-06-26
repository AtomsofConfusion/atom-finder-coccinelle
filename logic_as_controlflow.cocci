@script:python@
@@
from pathlib import Path
processed = {}
debug = False
ATOM_NAME = "assignment-as-value"

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
        subset = any(is_subset(new_range, existing) for existing in processed[start_line])
        if not subset:
            processed[start_line].append(new_range)
            processed[start_line] = [existing for existing in processed[start_line] if not is_subset(existing, new_range)]
            print_expression_and_position(exp, position, rule_name)
    else:
        processed[start_line] = [new_range]
        print_expression_and_position(exp, position, rule_name)

def is_subset(current, previous):
    # Check if the current range is entirely within the previous range
    if (current['start_line'] > previous['start_line'] or
        (current['start_line'] == previous['start_line'] and current['start_col'] >= previous['start_col'])) and \
       (current['end_line'] < previous['end_line'] or
        (current['end_line'] == previous['end_line'] and current['end_col'] <= previous['end_col'])):
        return True
    return False

@rule01@
identifier fun;
identifier F;
expression e;
identifier i;
type t;
type t_a;
position p;
assignment operator aop;
@@

(
t fun@F@p (..., t_a *i,... ) {
  ...
  *i aop e
  ...
}
)

@rule1@
expression e1, e2;
expression E;
binary operator bop = {&&, ||};
assignment operator aop;
identifier i;
position p;
@@

(
e1 bop@E@p <+... i++ ...+>
|
e1 bop@E@p <+... i-- ...+>
|
e1 bop@E@p <+... ++i ...+>
|
e1 bop@E@p <+... --i ...+>
|
e1 bop@E@p <+... i aop e2 ...+>
)

@script:python@
E << rule1.E;
p << rule1.p;
@@

//print("Rule1: ")
//print(f"   E:  {E}")
//print(f"       Line: {p[0].line}, Col: {p[0].column} - {p[0].column_end}")
print_if_not_contained(E, p)

@rule2@
position p;
binary operator bop = {||, &&};
identifier fun = rule01.F;
expression e;
expression E;
@@

(
e bop@E@p <+... fun(...) ...+>
)

@script:python@
E << rule2.E;
p << rule2.p;
@@

//print("Rule2: ")
//print(f"   E:  {E}")
//print(f"       Line: {p[0].line}, Col: {p[0].column} - {p[0].column_end}")
print_if_not_contained(E, p)