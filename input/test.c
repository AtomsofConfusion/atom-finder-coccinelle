#include <stdio.h>

int main() {
  int a;
  a = 1;
  a = 2;
  a = 3;
  printf("%d", a);
  int c = 2;
  int b = 0;

  a = a + 1;
  a += 1;
  a++;
  ++a;

  if (a == c) {
    printf("a == c");
  } else {
    a = a + 1;
  }

  if (a != c) { //excluded if with "neg_if"
    a = a + 1;
  } else {
    printf("a == c");
  }

  if (a > c) 
    printf("a > c");

  return 0;
}