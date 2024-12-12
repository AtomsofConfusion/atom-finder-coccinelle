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

void assignments() {
    // Safe Conversion: int to double
    int i1 = 10;
    double d1 = 9.5;
    int i2 = 5;
    i2 = d1;
    i2 = d1 + 10;
    i2 = 5 * d1 - 10;
    double d2 = 10.5;
    d2 = i1 + d1;
    i1 = i2 + 10;
    i2 = i1 + d1;

}

void binaruOperators() {
 // Initial variables of various types
    int i = 20;
    int i1 = 30;
    double d = 2.71;
    double d1 = 3.14;
    unsigned int ui = 4294967200U;  // Near the upper limit for 32-bit unsigned int
    float f = 5.5f;

    // Using integer and floating-point constants in calculations
    double calculationWithIntConst = (d * i1 + 50) / 2.0;  // Mixing double, int, and double constant
    double calculationWithFloatConst = (d + f * 25.0f) / 3.5;  // Float constant in mixed calculation

    // Using hexadecimal and scientific notation constants
    unsigned int hexConstCalculation = ui + 0xFF;  // Adding hexadecimal constant
    double sciConstCalculation = (d1 * 1.0e2) + 0x1A;  // Scientific notation and hexadecimal

    // Complex expression with multiple types and constants
    double multiTypeCalc = ((double)(i + 300) * 3.5 + ui) / d1;  // Mixed int, double, unsigned int with int constant

    // Dynamic updates involving constants
    i += 10;
    d *= 1.1;

    // More complex mixed type updates
    f += (float)(i1 + 20) / 2.5f;  // Increment float by the result of int division and conversion
}


void calculateMixedTypeExpressions() {
  int i1 = 10.5;
  int i2 = 5 + 10.5 + 5;
  i1 = 15.4;
  i1 = 5 + 15.3;
  double d = 2.0;
  d = 2.5;
}



void fun1(int x) {
  x = x + 1;
  double y = 1.5;
}

int fun2() {
  double x = 1.5;
  return x;
}

int fun2_1() {
  short x = 1;
  return x;
}

void fun3(int x, double y){
  x = y;
}

int main() {
  //Function call expression 
  double a1 = 1;
  double a2 = 1.5;
  int i1 = 1;
  short s1 = 1;
  fun1(a2);
  fun1(i1);
  fun(s1);
  fun3(a1, a2);
  fun3(a2, a1);
  declarations();
  calculateMixedTypeExpressions();

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