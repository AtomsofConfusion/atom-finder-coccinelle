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

  return 0;
}