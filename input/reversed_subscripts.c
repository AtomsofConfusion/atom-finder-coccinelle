#include <stdio.h>

int main() {

  int arr_int[5] = {1, 2, 3, 4, 5};
  int arr_int_2[3][3] = {{1, 1, 1}, {2, 2, 2}, {3, 3, 3}};
  char arr_char[5] = {'a', 'b', 'c', 'd', 'e'};
  char arr_char_2[3][3] = {{'a', 'a', 'a'}, {'b', 'b', 'b'}, {'c', 'c', 'c'}};
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

  int r12 = 1[arr_int_2[1]];
  int r13 = 1[2[arr_int_2]];

  return 0;
}