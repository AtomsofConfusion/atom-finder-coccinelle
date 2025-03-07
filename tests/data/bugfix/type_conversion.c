
#include <stdio.h>

int type_conversion() {
    unsigned a = 4;
    unsigned b = 2;
    unsigned c = 3;
    unsigned d = 4;
    int e = 5;

    if (a < 2) {
        print("this is fine");
    }

    if (a < 0) {
        print("this will never happen");
    }

    if (a + 3 && b < 0 ) {
        print("this will never happen");
    }

    if (c < 0 || a + 4) {
        print("shouldn't compare unsigned to 0");
    }

    if (c + 2 || a + 4 && d < 0) {
        print("shouldn't compare unsigned to 0");
    }

    if (c < 0 && d < 0) {
        print("shouldn't compare unsigned to 0");
    }

    if (e  < 0) {
        print("this is fine, this is an integer");
    }


    return 0;
}



