#include <stdio.h>

#define M1 64-1
#define M2 (64 - 1)
#define MF1(x) (2 * x)
#define MF2(x) (x + x)

int main() {
    int i = 1;
    int j = 1;
    int r1 = 2 * M1;
    int r2 = 2 * M2;
    int r3 = M1 * 2;
    int r4 = M2 * 2;
    int r5 = MF1(i++);
    int r6 = MF2(j++);
    printf("The result is: %d\n", r1);
    printf("The result is: %d\n", r2);
    printf("The result is: %d\n", r3);
    printf("The result is: %d\n", r4);
    printf("The result is: %d\n", r5);
    printf("The result is: %d\n", r6);
    
    return 0;
}
