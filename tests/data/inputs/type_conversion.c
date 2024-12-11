#include <stdio.h>


void declarations() {
    // Safe Conversion: int to double
    int i1 = 10;
    double d1 = i1;

    // Confusing Conversion: double to int (loss of fractional part)
    double d2 = 123.456;
    int i2 = (int)d2;
    int i2_1 = d2;
    int i2_2 = d2 + 10 - 4;

    // Confusing Conversion: float to int (loss of fractional part)
    float f1 = 9876.54321f;
    int i6 = (int)f1;

    // Safe Conversion: char to int
    char c1 = 'A';
    int i5 = c1;

    // Confusing Conversion: negative int to unsigned int
    int i4 = -1;
    unsigned int ui2 = (unsigned int)i4;

    // Safe Conversion: unsigned int to long long
    unsigned int ui1 = 4294967295;
    long long ll1 = ui1;

    // Confusing Conversion: long long to short (potential data loss)
    long long ll2 = 9223372036854775807;
    short s1 = (short)ll2;

    // Confusing Conversion: double to short (loss of precision and potential data loss)
    double d3 = 3.14e5;  // 314000
    short s2 = (short)d3;

    // Safe Conversion: short to int (no data loss)
    short s3 = 32767;
    int i7 = s3;
}

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
  declarations();

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