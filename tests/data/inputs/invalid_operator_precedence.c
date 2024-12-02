#include <stdio.h>

int main() {
  int a = 1;
  int b = 2;
  int c = 3;

  a || b & c;

  a || b ^ c;

  a || b + c;

  a || b - c;

  a || b << c;

  a && b | c;

  a && b + c;

  a && b - c;

  a && b << c;

  a || b && c;

  (a || b) && c; // should not include this non-confusing

  return 0;
}
