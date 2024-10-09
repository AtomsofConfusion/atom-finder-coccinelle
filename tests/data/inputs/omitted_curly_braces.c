#include <stdio.h>

int main() {
    int x = 0;
    int y = 5;

    if (x < y-1)
        printf("'if' without braces");
    
    if (x > y)
        printf("if without braces");

    if (x < y)
        printf("'if' without braces before an else");
    else 
        printf("'else' without braces after if without braces");

    if (x > y) {
        printf("'if' with braces before else without braces");
    } else
        printf("'else' without braces after if with braces");

    if (x > y) 
        printf("'if' wuthout braces with an else after it"); //R1 with neg_if
    else {
        printf("'else' with braces after if without braces");
    }

    if (x > y)
        printf("if without curly braces"); // note that coccinelle detects this structure as two parts, possibly due to two "if"s 
    else if (x < y)
        printf("else if without curly braces");
    
    if (x > y) {
        printf("if with curly braces");
    } else if (x < y) {
        printf("else if with curly braces");
    }

    // if - else if - else
    if (x > y) {
        printf("if with curly braces"); 
    } else if (x == y) {
        printf("else if with curly braces");
    } else {
        printf("else with curly braces");
    }

    if (x > y) 
        printf("if without curly braces");
    else if (x == y) 
        printf("else if without curly braces");
    else 
        printf("else without curly braces");

    // if - else if - else if - else
    if (x > 10) {
        printf("if with curly braces");
    } else if (x > 5) {
        printf("else if with curly braces"); 
    } else if (x > 0) {
        printf("else if with curly braces");
    } else {
        printf("else with curly braces");
    }

    if (x > 10) 
        printf("if without curly braces");
    else if (x > 5) 
        printf("else if without curly braces"); 
    else if (x > 0) 
        printf("else if without curly braces");
    else 
        printf("else without curly braces");

    if (x > 10) {
        printf("if with curly braces");
    } else if (x > 9) {
        printf("else if with curly braces");
    } else if (x > 8) {
        printf("else if with curly braces");
    } else if (x > 7)
        printf("else if with curly braces");
    else if (x > 6)
        printf("else if with curly braces");
    else {
        printf("else with curly braces");
    }

    // nested if structure
    if (x > 15) {

        if (x > 19) {
            printf("nested if with curly braces");
        } else if (x > 18)
            printf("nested else if without curly braces");
        else if (x > 17)
            printf("nested else if without curly braces");
        else if (x > 16) {
            printf("nested else if with curly braces");
        } else if (x > 15) {
            printf("nested else if with curly braces");
        } else {
            printf("nested else without curly braces");
        }

    } else if (x > 10) {

        if (x > 9) {
            printf("nested if with curly braces");
        } else if (x > 8)
            printf("nested else if without curly braces");
        else if (x > 7)
            printf("nested else if without curly braces");
        else if (x > 6) {
            printf("nested else if with curly braces");
        } else if (x > 5) {
            printf("nested else if with curly braces");
        } else {
            printf("nested else without curly braces");
        }

    } else if (x > 5) {

        if (x > 4) {
            printf("nested if with curly braces");
        } else if (x > 3)
            printf("nested else if without curly braces");
        else if (x > 2)
            printf("nested else if without curly braces");
        else if (x > 1) {
            printf("nested else if with curly braces");
        } else if (x > 0) {
            printf("nested else if with curly braces");
        } else {
            printf("nested else without curly braces");
        }


    } else {

        if (x > -1) {
            printf("nested if with curly braces");
        } else if (x > -2)
            printf("nested else if without curly braces");
        else if (x > -3)
            printf("nested else if without curly braces");
        else if (x > -4) {
            printf("nested else if with curly braces");
        } else if (x > -5) {
            printf("nested else if with curly braces");
        } else {
            printf("nested else without curly braces");
        }

    }

    if (x > 15)

        if (x > 19) {
            printf("nested if with curly braces");
        } else if (x > 18)
            printf("nested else if without curly braces");
        else if (x > 17)
            printf("nested else if without curly braces");
        else if (x > 16) {
            printf("nested else if with curly braces");
        } else if (x > 15) {
            printf("nested else if with curly braces");
        } else {
            printf("nested else without curly braces");
        }

    else if (x > 10)

        if (x > 9) {
            printf("nested if with curly braces");
        } else if (x > 8)
            printf("nested else if without curly braces");
        else if (x > 7)
            printf("nested else if without curly braces");
        else if (x > 6) {
            printf("nested else if with curly braces");
        } else if (x > 5) {
            printf("nested else if with curly braces");
        } else {
            printf("nested else without curly braces");
        }

    else if (x > 5)

        if (x > 4)
            printf("nested if with curly braces");
        else if (x > 3)
            printf("nested else if without curly braces");
        else if (x > 2)
            printf("nested else if without curly braces");
        else if (x > 1) {
            printf("nested else if with curly braces");
        } else if (x > 0) {
            printf("nested else if with curly braces");
        } else {
            printf("nested else without curly braces");
        }

    else 

        if (x > -1) {
            printf("nested if with curly braces");
        } else if (x > -2)
            printf("nested else if without curly braces");
        else if (x > -3)
            printf("nested else if without curly braces");
        else if (x > -4) {
            printf("nested else if with curly braces");
        } else if (x > -5) {
            printf("nested else if with curly braces");
        } else {
            printf("nested else without curly braces");
        }

// loop
    while (x < 5)
        printf("'while' without braces, x: %d", x++);

    while (x < 10) {
        printf("'while' with braces, x: %d", x++);
    }

    for (int i = 0; i < 5; i++)
        printf("'for' iteration: %d", i);
    
    do {
        printf("do while iteration: %d", x++);
    } while (x < 15);

    do
        printf("do while iteration: %d", x++);
    while (x < 20);

    return 0;
}