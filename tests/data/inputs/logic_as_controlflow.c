#include <stdio.h>

int fun1() {
    return 1;
}

int fun2() {
    return 1;
}

int fun3 (int* a) {
  a++;
  return *a;
}

int fun4 (int a) {
  a++;
  return a;
}

int fun5 (int* a, int b) {
  int c;
  c = b || (*a += 2);
  return c;
}

int main() {
    int a = 5;
    int b = 4;
    int c = 3;
    int d = 2;
    int e = 1;

    a || b++ & c;

    a && c | --b;

    a && c + b-- & d;

    a || b;

    a || b && c;

    a || b++ & c;

    a && ++b;

    a || b || c++;

    a && b || c++ < 1;

    a && ++b & c;

    a || b-- || c-- && d++ || --e;

    a || b-- || ++c;

    a || fun1(); // no?

    a || !(b = fun1());

    a && (b += 2) || c++;

    int f = a || b-- || c-- && d++ || --e;

    int g = a || (b = fun1());

    if (a && b) {
        a = 6;
    } else if (!a || --a > b) {
        a = 7;
    }

    (a > b) && fun1() && fun2();

    (a > b) || fun1();

    b || fun3(&a);

    b || fun4(a);

    b && (c + fun5(&a, b)); // all of these

}
