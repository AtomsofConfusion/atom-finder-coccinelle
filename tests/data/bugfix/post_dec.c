
#include <stdio.h>

int post_decrement() {
    int a = 10;
    int b = a--;
    int c = 0;
    int d = 4;
    int array[5] = {1, 2, 3, 4, 5};

    while(b + c + a--) {
        print("inside the loop");
    }

    while(a--) {
        print("inside the loop");
        print("inside the loop");
    }

    while(a--) {
        array[a];
    }

    while(a-- >= 0) {
        print("inside the loop");
        array[a];
    }

    while(b || a--) {
        print("inside the loop");
        array[a];
    }
    
    while(b-- && a--) {
        print("inside the loop");
        array[a];
        array[b];
    }
    
    while(a-- >= 0 && b ) {
        print("inside the loop");
        array[a];
    }

    while(b && a-- >= 0 ) {
        print("inside the loop");
        array[a];
    }

    while(b-- && c && a-- && d + 4) {
        array[a];
        array[b];
        print("inside the loop");
    }

    while(b && c && a-- >=0 && d) {
        array[a];
        print("inside the loop");
    }

    return 0;
}



