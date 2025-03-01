#include <stdio.h>

void fun1(int x) {
  x = x + 1;
  double y = 1.5;
}

int fun2() {
  double x = 1.5;
  return x;
}

void fun3(int x, double y){
  x = y;
}

int main() {
  //Function call expression 
  double a1 = 1;
  double a2 = 1.5;
  fun1(a2);
  fun3(a1, a2);
  fun3(a2, a1);


  long d1 = 0;
  long d2 = 1;

  if (d2 > 0) {
    printf("test");
  }

  if (!d1 || d2 > 0) {
      printf("The condition was true.\n");
  } else {
      printf("The condition was false.\n");
  }



  //Binary expression
  int b1 = 1;
  double b2 = 1.5;
  int b3 = b1 + b2;
  b3 += b2;
  1 + (int) 1.5;
  (int) 1.5 + 1;
  1.5 * 2;

  //not an atom
  double c1 = 1.0;
  double c2 = c1;

  //Simple declaration
  int e1 = 1;
  double e2 = e1;
  int e3 = 1.5;
  e1 = 1.5;
  double e4 = e1 + 4;

  double abc = 2.0;
  abc = 2.5;

  //Return statement
  func2();

  //Cast expression
  double g1 = 1.5;
  int g2 = (int)g1;
  

  return 0;
}
