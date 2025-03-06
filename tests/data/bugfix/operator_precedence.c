#include <stdio.h>

int main() {
    int a = 4, b = 5, c = 2;
    int result;

    // Example 1: ! and &
    // Potentially Confusing
    result = !a & b;  // Might be read as (!a) & b
    printf("Result of !a & b: %d\n", result);

    // Clear
    result = !(a & b);  // Clearly negating the result of a & b
    printf("Result of !(a & b): %d\n", result);

    // Example 2: & and <<
    // Potentially Confusing
    result = a & b << c;  // Might be read as a & (b << c)
    printf("Result of a & b << c: %d\n", result);

    result = a << b & c; 
    // Clear
    result = (a & b) << c;  // Clear grouping of & and <<
    printf("Result of (a & b) << c: %d\n", result);

    // Example 3: ! and >>
    // Potentially Confusing
    result = !a >> b;  // Might be read as (!a) >> b
    printf("Result of !a >> b: %d\n", result);

    // Clear
    result = !(a >> b);  // Clearly negating the result of a >> b
    printf("Result of !(a >> b): %d\n", result);

    // Example 4: + and ?
    // Potentially Confusing
    result = a + b ? c : 100;  // Might be misread without grouping context
    printf("Result of a + b ? c : 100: %d\n", result);

    // Clear
    result = (a + b) ? c : 100;  // Clear intention of condition
    printf("Result of (a + b) ? c : 100: %d\n", result);

    // Example 5: | and ?
    // Potentially Confusing
    result = a | b ? c : 100;  // Could be confusing without parentheses
    printf("Result of a | b ? c : 100: %d\n", result);

    // Clear
    result = (a | b) ? c : 100;  // Explicit conditional expression
    printf("Result of (a | b) ? c : 100: %d\n", result);

    // Example 6: & and ?
    // Potentially Confusing
    result = a & b ? c : 100;  // Might be unclear without grouping
    printf("Result of a & b ? c : 100: %d\n", result);

    // Clear
    result = (a & b) ? c : 100;  // Clearly defined logical condition
    printf("Result of (a & b) ? c : 100: %d\n", result);

    // Example 7: ~ and |
    // Potentially Confusing
    result = ~a | b;  // Could be misread as negation applying to a or the expression
    printf("Result of ~a | b: %d\n", result);

    // Clear
    result = (~a) | b;  // Clearly applies negation to a first
    printf("Result of (~a) | b: %d\n", result);

    // Example 8: >> and *
    // Potentially Confusing
    result = a >> b * c;  // Might be read as a >> (b * c)
    printf("Result of a >> b * c: %d\n", result);

    // Clear
    result = (a >> b) * c;  // Explicit about shift first, then multiplication
    printf("Result of (a >> b) * c: %d\n", result);

    // Example 9: << and *
    // Potentially Confusing
    result = a << b * c;  // Might be read as a << (b * c)
    printf("Result of a << b * c: %d\n", result);

    result = a * b << c;  // Might be read as a << (b * c)

    // Clear
    result = (a << b) * c;  // Clear about order of operations
    printf("Result of (a << b) * c: %d\n", result);

    return 0;
}
