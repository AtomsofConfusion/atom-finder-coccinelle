@macro_def_rule@
identifier macro_name;
expression e;
@@


#define macro_name e

@macro_use_rule@
identifier macro_def_rule.macro_name;
position p;
expression e;
@@


macro_name@p


@script:python@
p << macro_use_rule.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")