#include <stdio.h>

int func1() {
    return 1;
}

int func2() {
    return 1;
}

int main() {
    int a = 5;
    int b = 4;
    int c = 3;

    a || b;

    a || b && c;

    a || b++;

    a && ++b;

    a || b || c++;

    a && b || c++;

    a || b-- || c;

    a || b-- || ++c;

    a || fun1();

    a || (b = fun1());

    if (a && b) {
        a = 6;
    } else if (!a || --a > b) {
        a = 7;
    }

    (a > b) && func1() && func2();
    (a > b) || func1();
    // if we have two function calls, is that an atom?
    // seems strange
}
