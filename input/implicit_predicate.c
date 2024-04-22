#include <stdio.h>
#include <stdbool.h>


int main() {
  int a = 1;
  int b = 3;

  if (a % b) {
    printf("1");
  }

  if (1 % 0) {
    printf("1");
  }

  if (a % b) { // this line cannot be matched
    a++;
    a--;
  } else if (4 % 2) {
    b++;
    b--;
  } 
  
  if (1 % 0 != 0) {
    printf("1");
  }

  if (1 % 0 == 0) {
    printf("1");
  }

  if (a % b != 0) {
    printf("1");
  }

  if (a % b == 0) {
    printf("1");
  }

  if (a == b) {
    printf("1");
  }

  if (a != b) {
    printf("1");
  }

  bool c = true;
  bool d = false;

  if (true || false) {
    printf("1");
  }

  if (true && false) {
    printf("1");
  }

  if (c || d) {
    printf("1");
  }

  if (c && d) {
    printf("1");
  }

  return 0;
}