#include <stdio.h>

int main() {
    int x = 0;
    int y = 5;

    if (x < y-1)
        printf("'if' without braces\n"); //R1
    
    if (x > y)
        printf("if without braces\n");

    if (x < y)  // this is currently not getting detected
        printf("'if' without braces before an else\n"); //R1
    else 
        printf("'else' without braces after if without braces\n");

    if (x > y) {
        printf("'if' with braces before else without braces\n");
    } else
        printf("'else' without braces after if with braces\n");

    if (x > y) 
        printf("'if' wuthout braces with an else after it\n"); //R1 with neg_if
    else {
        printf("'else' with braces after if without braces\n");
    }

    if (x > y)
        printf("if without curly braces\n"); //R1
    else if (x < y)
        printf("else if without curly braces\n"); //R1
    
    if (x > y) {
        printf("if with curly braces\n");
    } else if (x < y) {
        printf("else if with curly braces\n");
    }

    while (x < 5)
        printf("'while' without braces, x: %d\n", x++);

    while (x < 10) {
        printf("'while' with braces, x: %d\n", x++);
    }

    for (int i = 0; i < 5; i++)
        printf("'for' iteration: %d\n", i);

    return 0;
}