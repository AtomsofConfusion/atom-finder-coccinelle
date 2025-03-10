
#include <stdio.h>


int fun1(int v1) {
    return v1;
}

int post_decrement() {
    int a = 10;
    int b = a--;
    int c = 0;
    int d = 4;
    int array[5] = {1, 2, 3, 4, 5};

    while(a-- >= 0) {
        print("inside the loop");
        array[a];
    }

    while(a-- >= 0) {
        print("inside the loop");
        array[a] + b;
    }

    while(a-- >= 0) {
        print("inside the loop");
        func1(array[a] + b);
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
        fun1(a);
        print("inside the loop");
    }

    return 0;
}



