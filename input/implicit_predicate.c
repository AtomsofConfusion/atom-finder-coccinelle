#include <stdio.h>
#include <stdbool.h>

bool funWithIP(int a, int b, bool c);

int main() {

  int a = 1;
  int b = 2;
  bool c = true;
  bool d = false;

  bool e = a % b;
  bool f = a % b == 0;

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

  if (false) { // todo
    printf("if without implicit predicate\n");
  } else if (c) {
    printf("else if without implicit predicate\n");
  }

  if (a == b) { // todo
    printf("if without implicit predicate\n");
  } else if (a != b) {
    printf("else if without implicit predicate\n");
  }

  if (a + b == 3) {
    printf("if without implicit predicate\n");
  } else if (a + b != 3) {
    printf ("else if without implicit predicate\n");
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

  while (true) { //todo
    printf("while without implicit predicate\n");
    count++;
    if (count == 10) break;
  }

  do { //todo
    count--;
    printf("do while without implicit predicate\n");
    if (count == 0) break; 
  } while (c);

  for (int i = 10; i; i--) {
    printf("for loop with implicit predicate\n");
  }

  for (int i = 10; i > 0; i--) {
    printf("for loop without implicit predicate\n");
  }

  int res1 = add(a % b ? 1 : 2, 3);
  int res2 = add(a % b == 0 ? 1 : 2, 3);
  bool res3 = funWithIP(a, b, a % b);
  bool res4 = funWithIP(a, b, c);
  bool res5 = funWithIP(a, b, a % b == 0);

  return 0;
}

bool funWithIP(int a, int b, bool c) {
  a = a + 1;
  b = b + 1;
  bool d = a % b;

  return b % a;
}

bool funWithoutIP(int a, bool b) {
  a++;
  return b;
}

/*
todo:
All the cases that only have a single bool variable or value
Calling of functions that take a bool value as one of its args.
*/