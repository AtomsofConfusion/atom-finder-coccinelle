@script:python@
@@
from pathlib import Path
debug = False
ATOM_NAME = "repurposed_variable"

def print_expression_and_position(exp, position, rule_name=""):
    file_path = Path(position[0].file).resolve().absolute()
    if rule_name and debug:
        print(rule_name)
    exp = exp.replace('"', '""')
    start_line, start_col = position[0].line, position[0].column
    end_line, end_col = position[0].line_end, position[0].column_end

    print(f"{ATOM_NAME},{file_path},{start_line},{start_col},{end_line},{end_col},\"{exp}\"")


@rule1@
position p;
type tf, ti;
identifier fun, i;
assignment operator a;
expression e;
expression E;
@@

  tf fun(..., ti i, ...) {
<...
(
i a@E@p e
|
i++@E@p
|
i--@E@p
)
...>
}

@script:python@
p << rule1.p;
E << rule1.E;
@@

print_expression_and_position(E, p, "Rule 1")

@rule2@
position p;
type tf, ti;
identifier fun, i;
assignment operator a;
expression e;
expression E;
@@

(
  tf fun(..., ti i, ...) {
    <...
    ++i@E@p
    ...>
  }
)


@script:python@
p << rule2.p;
E << rule2.E;
@@

print_expression_and_position(f"++{E}", p, "Rule 2")


@rule3@
position p;
type tf, ti;
identifier fun, i;
assignment operator a;
expression e;
expression E;
@@

(
  tf fun(..., ti i, ...) {
    <...
    --i@E@p
    ...>
  }
)


@script:python@
p << rule3.p;
E << rule3.E;
@@

print_expression_and_position(f"--{E}", p, "Rule 3")
