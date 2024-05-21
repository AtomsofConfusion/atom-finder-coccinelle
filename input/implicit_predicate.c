#include <stdio.h>

struct s {
  int s_i;
};

int main() {

  int a = 1;
  int b = 2;

  struct s c = {3};

  char ip1 = a % b ? '0' : '1';
  char ip2;
  ip2 = b % a ? '0' : '1';
  char nip1 = a % b == 0 ? '0' : '1';
  char nip2;
  nip2 = a == b ? '0' : '1';

  if (a % b) {
    printf("if with implicit predicate\n");
  } else if (b % a) {
    printf("else if with implicit predicate\n");
  }

  if (a == b) {
    printf("if without implicit predicate\n");
  } else if (a != b) {
    printf("else if without implicit predicate\n");
  }

  if (a + b == 3) {
    printf("if without implicit predicate\n");
  } else if (a + b != 3) {
    printf ("else if without implicit predicate\n");
  }

  if (add(1, 2)) {
    printf("if with implicit predicate\n");
  } else if (add(a, b)) {
    printf("else if with implicit predicate\n");
  }

  int count = 10;

  while (count) {
    printf("while with implicit predicate\n");
    count--;
  }

  count = 10;

  do {
    printf("do while with implicit predicate\n");
    count--;
  } while (count);

  count = 10;

  while (count > 0) {
    printf("while without implicit predicate\n");
    count--;
  }

  count = 10;

  do {
    printf("do while without implicit predicate\n");
    count--;
  } while (count > 0);

  for (int i = 10; i; i--) {
    printf("for loop with implicit predicate\n");
  }

  for (int i = 10; i > 0; i--) {
    printf("for loop without implicit predicate\n");
  }

  int res1 = add(a % b ? 1 : 2, 3);
  int res2 = add(a % b == 0 ? 1 : 2, 3);

  //nested cases
  if (add(a % b ? 1 : 2, 3)) {
    printf("if and ternary operator with implicit predicate\n");
  } else if (add(a % b ? 1 : 2, 3) == 1) {
    printf("ternary operator with implicit predicate\n");
  } else if (add(a % b != 0 ? 1 : 2, 3) == 1) {
    printf("else if and ternary operator without implicit predicate\n");
  }

  count = 0;
  
  while (add(count, count ? 1 : 10)) {
    printf("while with implicit predicate\n");
    count--;
  }

  do {
    printf("do while with implicit predicate\n");
    count++;
  } while (add(count, count ? -1 : 0));

  while (add(count, count != 0 ? 1 : 10) != 0) {
    printf("while without implicit predicate\n");
    count--;
  }

  do {
    printf("do while without implicit predicate\n");
    count++;
  } while (add(count, count == 0 ? -1 : 0) != 0);

  for (int i = 0; add(i, i & 3 ? 1 : -i); i++) {
    printf("for with implicit predicate\n");
  }

  for (int i = 1; add(i, i & 3 != 0 ? 1 : -i) > 0; i++) {
    printf("for with implicit predicate\n");
  }
  
  return 0;
}

int fun1 (struct s *c) {
  int funi = c -> s_i ? 1 : 2;
  if (c -> s_i) {
    return 1;
  }
  return 2;
}