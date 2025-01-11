
#include <stdio.h>

int pre_increment() {
    int a = 10;
    // this is an atom
    int b = ++a;
    int c = 0;
    // this is not an atom
    b++;
    // these two are atoms
    b = 1 - 10 + ++b + 3;
    c = ++b;
    
    // this is not an atom
    for(int i = 0; i < 5; ++i) {
        printf("Loop iteration: %d\n", i);
    }
    
    printf("Value of a: %d\n", a);
    printf("Value of b: %d\n", b);
    
    return 0;
}


int pre_decrement() {
    int a = 10;
    // this is an atom
    int b = --a;
    int c = 0;
    // this is not an atom
    --b;
    // these two are atoms
    b = 1 - 10 + --b + 3;
    c = --b;
    
    // this is not an atom
    for(int i = 0; i < 5; --i) {
        printf("Loop iteration: %d\n", i);
    }
    
    printf("Value of a: %d\n", a);
    printf("Value of b: %d\n", b);
    
    return 0;
}




