@non_atoms@
expression e,x;
statement S;
type t;
identifier i;
position p;
@@

// this does not work because ++ and -- are Coccinelle's tranformations
(
++e
|
--e
)

