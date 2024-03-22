#include <stdio.h>

int main() {
    int v1, v2, v3;
    // Regular assignments
    v1 = 5;
    v2 = 7;
    v3 = 10;

    v1 = v2 = v3 + 5;


    v1 = v2 = v3 = 5;

    printf("v1: %d, v2: %d\n", v1, v2);

    return 0;
}
