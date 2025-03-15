#include <stdio.h>

int main() {
    int a = 2, b = 3, c = 4, d = 5;

    int result1 = a * b << c;
    int result2 = a << b * c;
    int result3 = a & b << c;
    int result4 = a << b & c;

    int result5 = a + b ? c : d;
    int result6 = a | b ? c : d;
    int result7 = a & b ? c : d;

    int result8 = ~a | b;
    int result9 = a >> b * c;
    int result10 = a << b * c;

    int result11 = (a * b) << c;
    int result12 = a << (b * c);
    int result13 = (a & b) << c;
    int result14 = a << (b & c);

    int result15 = (a + b) ? c : d;
    int result16 = (a | b) ? c : d;
    int result17 = (a & b) ? c : d;

    int result18 = (~a) | b;
    int result19 = a >> (b * c);
    int result20 = a << (b * c);
    int result21 = ~(a | b);

    return 0;
}
