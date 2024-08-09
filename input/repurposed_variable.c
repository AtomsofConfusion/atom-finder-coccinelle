#include <stdio.h>

int fun1(int a) {
  a = 1;
  a += 2;
  a++;
  return a;
}

int fun2(int a) {
  int b = a;
  return b;
}

int fun3(int* a) {
  *a = 1;
  return 1;
}

int fun4(int a) {
  if (a > 0) {
    a = 3;
  } 
  
  if (a > 0) {
    a = 3;
  } else if (a < 0) {
    a = -3;
  } else {
    a = 0;
  }
  
  return a;
}

int main() {
  return 0;
}