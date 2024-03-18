#include <stdio.h>

int main() {
    int x = 0;
    int y = 5;

    if (x < y)
        printf("'if' without braces\n");

    if (x > y) {
        printf("'if' with braces\n");
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