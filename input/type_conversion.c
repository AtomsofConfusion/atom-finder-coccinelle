#include <stdio.h>

void fun1(int x) {
  x = x + 1;
}

int fun2() {
  double x = 1.5;
  return x;
}

void fun3(int x, double y){
  x = x + 1;
  y = y + 0.5;
}

int main() {
  //Function call expression 
  double a1 = 1;
  double a2 = 1.5;
  fun1(a2);
  fun3(a1, a2);
  fun3(a2, a1);

  //Binary expression
  int b = 1;
  double c = 1.5;
  int d = b + c;

  //Simple declaration
  int e = 1;
  double f = e;

  //Return statement
  func2();

  //Cast expression
  double g = 1.5;
  int h = (int)g;
  

  return 0;
}