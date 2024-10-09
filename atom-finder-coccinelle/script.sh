#!/bin/bash

spatch -sp_file cocci/assignment_as_value.cocci tests/data/inputs/assignment_as_value.c > cocci_outputs/assignment_as_value.csv
spatch -sp_file cocci/change_of_literal_encoding.cocci tests/data/inputs/change_of_literal_encoding.c > cocci_outputs/change_of_literal_encoding.csv
spatch -sp_file cocci/comma_operator.cocci tests/data/inputs/comma_operator.c > cocci_outputs/comma_operator.csv
spatch -sp_file cocci/conditional_operator.cocci tests/data/inputs/conditional_operator.c > cocci_outputs/conditional_operator.csv
spatch -sp_file cocci/implicit_predicate.cocci tests/data/inputs/implicit_predicate.c > cocci_outputs/implicit_predicate.csv
# spatch -sp_file cocci/operator_precedence.cocci tests/data/inputs/invalid_operator_precedence.c > cocci_outputs/invalid_operator_precedence.csv
spatch -sp_file cocci/logic_as_controlflow.cocci tests/data/inputs/logic_as_controlflow.c > cocci_outputs/logic_as_controlflow.csv
# spatch -sp_file cocci/macro_operator_precedence.cocci tests/data/inputs/macro_operator_precedence.c > cocci_outputs/macro_operator_precedence.csv
# spatch -sp_file cocci/operator_precedence.cocci tests/data/inputs/macro_test.c > cocci_outputs/macro_test.csv
spatch -sp_file cocci/omitted_curly_braces.cocci tests/data/inputs/omitted_curly_braces.c > cocci_outputs/omitted_curly_braces.csv
# spatch -sp_file cocci/operator_precedence.cocci tests/data/inputs/operator_precedence.c > cocci_outputs/operator_precedence.csv
spatch -sp_file cocci/post_incdec.cocci tests/data/inputs/post_incdec.c > cocci_outputs/post_incdec.csv
spatch -sp_file cocci/pre_incdec.cocci tests/data/inputs/pre_incdec.c > cocci_outputs/pre_incdec.csv
spatch -sp_file cocci/repurposed_variable.cocci tests/data/inputs/repurposed_variable.c > cocci_outputs/repurposed_variable.csv
spatch -sp_file cocci/reversed_subscripts.cocci tests/data/inputs/reversed_subscripts.c > cocci_outputs/reversed_subscripts.csv
spatch -sp_file cocci/type_conversion.cocci tests/data/inputs/type_conversion.c > cocci_outputs/type_conversion.csv