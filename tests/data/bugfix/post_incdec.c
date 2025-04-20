
#include <stdio.h>

void test0() {

}

void test1() {
    int a = 5;
    while (a--) {
        printf("In loop: a = %d\n", a);
    }

    if (a) {
        printf("After loop, a is non-zero\n");
    }
}


void test2() {
    int a = 5;
    int b = 0;
    while (a--) {
        printf("In loop: a = %d\n", a);
    }

    b ++;
    printf("Unrelated code: b = %d\n", b);

    if (a) {
        printf("After loop, a is non-zero\n");
    }
}

void test3() {
    int a = 3, b = 1;
    while (a-- && b) {
        printf("test3 - In loop: a = %d, b = %d\n", a, b);
    }

    if (a) {
        printf("test3 - After loop, a is non-zero\n");
    }
}

void test4() {
    int x = 1, a = 3, y = 1;
    while (x && a-- && y) {
        printf("test4 - In loop: a = %d\n", a);
    }

    if (a) {
        printf("test4 - After loop, a is non-zero\n");
    }
}
    
void test5() {
    int x = 1, y = 1, a = 3;
    while (x && y && a--) {
        printf("test5 - In loop: a = %d\n", a);
    }

    if (a) {
        printf("test5 - After loop, a is non-zero\n");
    }
}

void test6() {
    int a = 0, b = 3;
    while (a-- || b--) {
        printf("test6 - In loop: a = %d, b = %d\n", a, b);
    }

    if (a) {
        printf("test6 - After loop, a is non-zero\n");
    }
}

void test7() {
    int a = 0, b = 3;
    while (b-- || a--) {
        printf("test7 - In loop: a = %d, b = %d\n", a, b);
    }

    if (a) {
        printf("test7 - After loop, a is non-zero\n");
    }
}

void test8() {
    int a = 5;
    while (a--) {
        printf("test8 - In loop: a = %d\n", a);
    }

    a = 10;
    if (a) {
        printf("test8 - After reassignment, a is non-zero\n");
    }
}

void test9() {
    int a = 5;
    while (a--) {
        printf("test9 - First loop: a = %d\n", a);
    }

    while (a--) {
        printf("test9 - Second loop: a = %d\n", a);
    }

}

void test10() {
    int a = 5;
    int b = 6;
    while (a--) {
        printf("test10 - First loop: a = %d\n", a);
    }

    while (b || a--) {
        printf("test10 - Second loop: a = %d\n", a);
    }

    if (a) {
        printf("test10 - After reassignment, a is non-zero\n");
    }

}

void test11() {
    int a = 3;
    while (a--) {
        printf("test11 - In loop: a = %d\n", a);
    }

    if (a > 0) {
        printf("test11 - a > 0\n");
    }
}

void test12() {
    int a = 3;
    while (a--) {
        printf("test12 - In loop: a = %d\n", a);
    }

    if (a == 0) {
        printf("test12 - a == 0\n");
    }
}

void test13() {
    int a = 3;
    while (a--) {
        printf("test13 - In loop: a = %d\n", a);
    }

    if (a < 0) {
        printf("test13 - a < 0\n");
    }
}

void test14() {
    int a = 3;
    while (a--) {
        printf("test14 - In loop: a = %d\n", a);
    }

    if (a == -1) {
        printf("test14 - a == -1\n");
    }
}

void test15() {
    int a = 4;
    int b;
    int c;
    int arr[] = {10, 20, 30, 40, 50};

    while (a-- >= 0) {
        printf("test15");
        b = arr[a];
        c = arr[a];
    }

}

struct container {
    int arr[5];
};

void test17() {
    struct container c = { .arr = {100, 200, 300, 400, 500} };
    struct container *ptr = &c;

    int a = 4;
    while (a-- >= 0) {
        ptr->arr[a];
    }
}

void test18() {
    int a = 3;
    int c;
    while (a--) {
        printf("test18 - In loop: a = %d\n", a);
    }

    int c = a + 4;
    if (a) {
        printf("test18");
    }

    return a;

}


int main() {
    test1();
    test2();
    return 0;
}
