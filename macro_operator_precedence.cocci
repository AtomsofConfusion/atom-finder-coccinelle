//macro definitions might be in header files
//so we need to make sure those are included
@macro_def_rule@
identifier macro_name;
expression e1, e2;
binary operator bop;
@@

// (e1 bop e2) is not a problem, but no parathesis is
#define macro_name e1 bop e2

@macro_use_rule@
identifier macro_def_rule.macro_name;
position p;
expression e;
binary operator bop;
@@


(
e bop macro_name@p
|
macro_name@p bop e
)



@script:python@
p << macro_use_rule.p;
@@

print(f"Line {p[0].line} in file {p[0].file}")