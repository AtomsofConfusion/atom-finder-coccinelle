#include <stdio.h>

int main() {
  int a;
  a = 1;
  a = 2;
  a = 3;
  printf("%d", a);
  int c = 2;
  int b = 0;

  a = a + 1;
  a += 1;
  a++;
  ++a;

//
  for (int k = 0; k < 10; k++) { //can be matched by "for(...;...;i++)" and "for(...;...;++i)" and "for(int i = 0;...;i++)"
    printf("%d\n", k);
  }

  for (int k = 0; k < 10; ++k) {//can be matched by "for(...;...;i++)" and "for(...;...;++i)" and "for(int i = 0;...;++i)"
    printf("%d\n", k);
  }
  //these two above have the isomorphism of increment.(valid in for loop). "for_inc" can disable this kind of isomorphism

  for (int k = 0; k < 10; k = k + 1) {
    printf("%d\n", k);
  }

  for (int k = 0; k < 10; k += 1) {
    printf("%d\n", k);
  }

//
  if (a == c) {
    printf("a == c");
  } else {
    a = a + 1;
  }

  if (a != c) { //excluded if with "neg_if"
    a = a + 1;
  } else {
    printf("a == c");
  }
//these two above have isomorphism of if structure

  if (a > c) {
    printf("a > c");
  } else if (a < c) {
    printf("a < c");
  }

  if (a > c) {
    printf("a > c");
  } else if (a < c) {
    printf("a < c");
  } else {
    printf("a = c");
  }

  if (a > c) {
    printf("a > c");
  } else if (a > 1) {
    printf("a > 1");
  } else if (a == c) {
    printf("a = c");
  } else {
    printf("else");
  }

  if (a > c) 
    printf("a > c");

  return 0;
}


//https://coccinelle.gitlabpages.inria.fr/website/standard.iso.html