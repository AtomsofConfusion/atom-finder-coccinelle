#include <stdio.h>

int func() {
    return 1;
}

int main() {
    int a = 5;
    int b = 4;

    (a > b) && func();
    // if we have two function calls, is that an atom?
    // seems strange
}
