#include <stdio.h>

int add(int a, int b);

int main() {
    int v1, v2, v3, v4;
    v1 = 5;
    v2 = 7;
    v3 = 10;

    v1 = v2 = v3 + 5;

    v1 = v2 = v3 = 5;

    v1 = v2 = v3 = v4 = 10;

    v1 += v2 -= v3;

    printf("v1: %d, v2: %d\n", v1, v2);

    int v5 = v1 = 6;

    int v6 = v2 = v3 = v4 = 7;

    int v7 = v1 == v2;

    int v8;
    v8 |= v6 = add(v1, v2);

    int v9;
    v9 = v1 += (v2 -= 4);

    int v10 = (v1 += v2);
    int v11 = v1 += (v2 -= v3);
    int v12 = (v1 += (v2 -= v3));
    int v13;
    v12 = v3 + (v1 -= 2);
    v1 = v2 += v3 - (v4 += 2);
    v1 = (v2 += v3 - (v4 += 2));
    v1 = v2 + (v3 -= v4 += 2);
    v1 = v2 + v3 + (v4 += v5);

    for (int i = 0; v1 = v2 = i < 5; v3 = v4 -= 2, i++) {
        printf("%d\n", i);
    }

    for (int i = v5 = 0; i < 5; i++) {
        printf("%d\n", i);
    }

    for (int i = (v1 += v3 = 2); i < 10; i++) {
        printf("%d\n", i);
    }

    while (v1 < 5, v3 += v1) {
        v1++;
    }

    while (add(1, 3), v1 = v3 += v4 - 1, v1 > 0 && v1 < 10) {
        printf("%d\n", v1);
    }

    while (v1 += v2 = 2) {
        if (v1 >= 20) {
            break;
        }
    }

    if (v1 < 10, v1 += 5) {
        v2 -= 2;
    }

    if (v1 < 10, v2 += 5) {
        v3 = v4 -= v6 = 2;
    } else if (v2 < 10, v1 += 5) {
        printf("%d\n", v2);
    } else if (v3 < 10, v4 = v3) {
        printf("%d\n", v4);
    }

    return 0;
}

int add(int a, int b) {
    return a + b;
}