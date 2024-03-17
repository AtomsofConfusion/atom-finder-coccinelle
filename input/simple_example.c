
#include <stdio.h>

int main() {
    int a = 10;
    // this is an atom
    int b = a++;
    b++;
    b = 1 - 10 + b++ + 3;
    
    // this is not an atom
    for(int i = 0; i < 5; i++) {
        printf("Loop iteration: %d\n", i);
    }
    
    printf("Value of a: %d\n", a);
    printf("Value of b: %d\n", b);
    
    return 0;
}
