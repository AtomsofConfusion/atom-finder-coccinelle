#include <stdio.h>

int main() {
    int a = 10, b = 20;
    int i = 0, j = 10;

    if (a < b)
        a++;
    else
        a--, 
    b--;

    while (a) a--, b--;


    // this is fine
    if (a < b) {
        a--, 
        b--;
    }
    
    // this is not
    if (a < b)
        a--, 
    b--;
    
    while (i < j)
        a ++;

    while (i < j)
        a--, 
    b--;

    for (i = 0; i < j; i ++ ){
        a--, 
        b--;
    }

    for (i = 0; i < j; i ++ )
        a--;
    b--;

    for (i = 0; i < j; i ++ )
        a--,
    b--;

    return 0;

}


