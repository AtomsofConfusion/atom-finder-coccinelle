#include <stdio.h>

int main() {
  int a =  1;
  int b = 2;
  
  if (a == b) {
    printf("1");
  }

  if (a == b) //Rule3
    printf("1");

  if (a == b) {
    printf("1");
  } else {
    printf("1");
  }

  if (a == b)
    printf("1");
  else {
    printf("1");
  }

  if (a != b) 
    printf("1");
  else {
    printf("1");
  }

  if (a == b) { //if we have "disable braces0, neg_if", rule1 will not match this 
    printf("1");
  } else 
    printf("1");

  if (a == b) 
    printf("1");
  else 
    printf("1");

  if (a == b) {
    printf("1");
  } else if (a < b) {
    printf("1");
  } else {
    printf("1");
  }

  if (a == b) 
    printf("1");
  else if (a < b) {
    printf("1");
  } else {
    printf("1");
  }

  if (a == b) {
    printf("1");
  } else if (a < b)
    printf("1");
  else {
    printf("1");
  }

  if (a == b) {
    printf("1");
  } else if (a < b) {
    printf("1");
  } else
    printf("1");
  
  if (a > 5) {
    printf("1");
  } else if (a > 4)
    printf("1");
  else if (a > 3) {
    printf("1");
  } else {
    printf("1");
  }

  if (a > 6) {
    printf("1");
  } else if (a > 5) 
    printf("1");
  else if (a > 4) 
    printf("1");
  else if (a > 1) 
    printf("1");
  else {
    printf("1");
  }

  if (a > 6) 
    printf("1");
  else if (a > 5) 
    printf("1");
  else if (a > 4)
    printf ("1");
  else if (a > 1)
    printf ("1");
  else 
    printf("1");
  
  
  return 0;
}

/*

*/