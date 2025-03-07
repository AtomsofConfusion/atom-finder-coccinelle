
#include <stdio.h>

int type_conversion() {
    unsigned a = 4;
    unsigned b = 2;
    unsigned c = 3;
    unsigned d = 4;

    if (a < 0) {
        print("this will never happen");
    }

    if (a + 3 && b < 0 ) {
        print("this will never happen");
    }

    if (c < 0 || a + 4) {
        print("should compare unsigned to 0");
    }

    if (c < 0 || a + 4 && d < 0) {
        print("should compare unsigned to 0");
    }


    return 0;
}



