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

    (a > b) && func1() && func2();
    (a > b) || func1();
    // if we have two function calls, is that an atom?
    // seems strange
}
