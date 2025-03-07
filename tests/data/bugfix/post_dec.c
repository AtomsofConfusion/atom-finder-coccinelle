
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
        array[a];
        print("inside the loop");
    }

    while(a-- >= 0) {
        print("inside the loop");
        array[a];
    }

    while(b && a--) {
        print("inside the loop");
        array[a];
    }
    
    while(a-- && b ) {
        print("inside the loop");
        array[a];
    }
    while(b && c && a-- && d) {
        array[a];
        print("inside the loop");
    }

    return 0;
}



