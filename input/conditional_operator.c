#include <stdio.h>
#include <stdbool.h>

struct S1 {
    int s1_v1;
};

struct S2 {
    struct S1* s2_s1;
};

int main() {
    int V1 = 3;
    int V3 = 5;

    struct S1 s1 = {
        V1
    };

    struct S2 s2 = {
        &s1
    };

    struct S2 *s2_p = &s2;

    int V2 = V1 == 3 ? 2 : 1;
    int V4 = V1 == 3 ? 2 : (V1 == 5 ? 3 : 1);
    int V5 = 0;

    V5 = V1 > 4 ? 10 : 20;

    int V6 = (V4 & V1) ? true : false;

    int res1 = s2_p->s2_s1 ? s2_p->s2_s1 -> s1_v1 : 0;
    int res2 = V1 < 32 ? (~0U >> V1) : ~0U;
    int res3 = !add(-1, V1) ? (V1 & V3) : V5;
    int res4 = (!V1 || V3) ? false : (V2 == V5);

    add(V1 % V2 ? 1 : 2, 3);

    for (int i = 1; add(i, (i & 3) != 0 ? 1 : -i) > 0; i++) {
        printf("for with conditional operator\n");
    }
    return 0;
}
