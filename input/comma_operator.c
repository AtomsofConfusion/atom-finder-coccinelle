#include <stdio.h>

int main() {
    int V1 = 5;
    int V2, V3;

    V3 = (V1++, V1);  // Increments V1, then assigns the incremented value of V1 to V3
    printf("V1 after increment: %d, V3: %d\n", V1, V3);

    V2 = 3;
    V3 = (V2++, V2 += 2, V2);  // Increments V2, adds 2 to V2, then assigns the final value of V2 to V3
    printf("V2 after operations: %d, V3: %d\n", V2, V3);

    return 0;
}
