#include <stdio.h>

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

    int v4 = v1 = 6;

    int v5 = v2 = v3 = v4 = 7;

    int v6 = v1 == v2;

    int v7;
    v7 |= v6 = add(v1, v2);

    int v8;
    v8 = v1 + (v2 -= 4);

    int v9 = (v1 += v2);
    int v10 = v1 += (v2 -= v3);
    int v11 = (v1 += (v2 -= v3));

    for (int i = 0; v1 = v2 = i < 5; v3 = v4 -= 2, i++) {
        printf("%d\n", i);
    }

    for (int i = v5 = 0; i < 5; i++) {
        printf("%d\n", i);
    }

    while (v1 < 5, v3 += v1) {
        v1++;
    }

    while (v1 = v3 += v4 - 1, v1 > 0 && v1 < 10) {
        printf("%d\n", v1);
    }

    return 0;
}
