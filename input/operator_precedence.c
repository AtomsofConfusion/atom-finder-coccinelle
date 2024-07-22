#include <stdio.h>

int main () {
  int a = 1;
  int b = 2;
  int c = 3;

  1 + 2 * 3;

  1 * 2 + 3;

  1 - 2 * 3;

  1 * 2 - 3;

  1 + 2 + 3 * 4 - 5 * 6;

  1 + 2 * (3 - 4 * 5) * 6;

  1 + (2 * 3);

  a + b * c;

  a + (b * c);

  a * b + c;

  a + 2 || 3 * b + 5 && c && 7;

  a & b || c;

  a | c && b;

  a ^ c || b;

  a % b && c;

  a && b % c;

  a && b * c;

  a * c && b;

  a - b && c;

  a + b && c;

  a << b && c;

  a ^ b && c;

  a ^ b | c;

  a | b ^ c;

  a || b && c;

  a && b ^ c;

  +a && b;

  return 0;
}