
#include <stdio.h>


int fun1(int v1) {
    return v1;
}

#include <stdio.h>

int testPostLoopAssignment(int a) {
    while (a--) {
        // Simulate some operations
    }
    a = 10; // Re-assignment after the loop
    return a;
}


int testCheckNegative(int b) {
    while (b--) {
        // Simulate some operations
    }
    if (b < 0) {
        printf("Variable b is negative after the loop: %d\n", b);
    }
    return b;
}

int testCheckExactNegativeOne(int c) {
    while (c--) {
        // Simulate some operations
    }
    if (c == -1) {
        printf("Variable c is exactly -1 after the loop: %d\n", c);
    }
    return c;
}

int testCheckExactNegativeOne(int d) {
    while (d--) {
        // Simulate some operations
    }
    if (2 && !d && 1) {
        printf("will not be true id d == -1");
    }
    return d;
}

int testCheckExactNegativeOne(int e) {
    while (e--) {
        // Simulate some operations
    }
    if (e == 0) {
        printf("will be true if e == -1");
    }
    return e;
}

int testCheckExactNegativeOne(int f) {
    while (f--) {
        // Simulate some operations
    }
    for (f=0; f < 5; f++){
        printf("for loop");
    }
    return f;
}

int testReturnExactlyVar(int g) {
    while (g--) {
        // Simulate some operations
    }
    return g;
}

int testRedefinition1() {
    int h = 5;
    while (h --) {
        printf("for loop");
    }
    return 0;
}

int testRedefinition2() {
    int h = 5;
    return h;
}

int post_decrement() {
    int a = 10;
    int b = a--;
    int c = 0;
    int d = 4;
    int array[5] = {1, 2, 3, 4, 5};

    int resultA = testPostLoopAssignment(5);

    int resultB = testCheckNegative(5);

    int resultC = testCheckExactNegativeOne(5);
}



