#include <stdio.h>

int main() {

    ~ 1;

    1 + 2;

    1 & 2;

    1 | ~2;

    1 ^ 2 + 3 - 4 >> ~5;

    1 ^ 2 + 3 ^ 4;

    1 + 2 & 3 | 4 * 5;

    13 ^ 5 | ~1000;

    0x1B & 076;

    0X1B | 076;

    0X1B | 076 & 0b1010 << 5;

    int a = 0xAB | 0xCD;

    int b = 0b1010 << 5;

    int c = 0B0001 >> 1;

    int d = 013 ^ 4;

    d <<= 12;

    int e = b |= 10;

    int f = a = c |= 9;

    for (int i = 3 & 0x3C; i > 10, a = 14 & ~0B1110; i--) {
        i += 2;
    }

    while (a < 10, b = 13 ^ 5 | ~1000) {
        a++;
    }

    if (10 | a) {
        a &= 0xA;
    } else if (5 ^ b) {
        b ^= 0B101;
    }

    return 0;
}