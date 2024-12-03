#include <stdio.h>

int main() {

  int arr_int[] = {1, 2, 3, 4, 5};
  char arr_char[] = {'a', 'b', 'c', 'd', 'e'};
  char str[] = "abcde";
  int i = 1;
  int x = 1;
  int y = 1;

  int r1 = arr_int[1];
  int r2 = 1[arr_int];
  char r3 = arr_char[i];
  char r4 = i[arr_char];
  char r5 = str[i++];
  char r6 = i++[str];
  char r7 = "abcde"[1];
  char r8 = 1["abcde"];
  int r9 = (1 + 2 - 1)[arr_int];
  char r10 = (1 + 2)[arr_char];
  char r11 = (x + y)["abcde"];

  return 0;
}