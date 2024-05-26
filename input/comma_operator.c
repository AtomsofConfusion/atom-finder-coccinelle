#include <stdio.h>

int main() {
    int v1 = 0;
    int v2 = 1;
    int v3 = 2;
    int v4, v5, v6;
    v4 = v1 + 3, v5 = v4 + v3, v6 = v2 - v5;
    v4 += v3;
    v4++, v5--, v6 + v1;
    v4 += v5 + v6, v5 -= v3;

    v1++, v2--, v3+=5;

    add(v1, v2); // make sure that this is not an atom

    int c1 = (v1--, v1);
    int c2 = (v1++, v2++, v1 + v2);
    int c3 = (v1--, v2, v3 % v2, (v1 - v2) * v3);
    int c4 = (~(int)0, ~(int)0);

    for (int i = 0; i < 10; i++) {
        printf("for loop without atom");
    }

    for (int i = 0; i < 10; i++, v2++, v3 = v4 - v2) {
        printf("for loop with atom");
    }

    while (v1 > 0) {
        v1--;
        printf("while loop without atom");
    }

    while (v2++, v1 = v3 - v2, v3 -= v2, v1 < 0) {
        printf("while loop with atom");
    }

    return 0;
}

int add(int a, int b) {
    return a + b;
}
