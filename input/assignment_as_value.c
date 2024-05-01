#include <stdio.h>

int main() {
    int v1, v2, v3, v4;
    // Regular assignments
    v1 = 5;
    v2 = 7;
    v3 = 10;

    v1 = v2 = v3 + 5;

    v1 = v2 = v3 = 5;

    v1 = v2 = v3 = v4 = 10;

    printf("v1: %d, v2: %d\n", v1, v2);

    int v4 = v1 = 6;

    int v5 = v2 = v3 + 1;

    // In specific structure
    for (int i = 0; i < 5; i++) {
        printf("%d\n", i);
    }

    for (int i = v5 = 0; i < 5; i++) {
        printf("%d\n", i);
    }

    return 0;
}
