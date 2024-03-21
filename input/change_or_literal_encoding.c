#include <stdio.h>

int main() {
    // Decimal constant
    int dec = 20;
    printf("Decimal: %d\n", dec);

    // Octal constant (prefix 0)
    int oct = 024; // Equivalent to 20 in decimal
    printf("Octal: %d (Octal input: 024)\n", oct);
    printf("Octal: %d (Octal input: 026)\n", 026);

    // Hexadecimal constant (prefix 0x or 0X)
    int hex = 0x14; // Equivalent to 20 in decimal
    printf("Hexadecimal: %d (Hex input: 0x14)\n", hex);
    printf("Hexadecimal: %d (Hex input: 0x16)\n", 0x16);

        // Hexadecimal constant (prefix 0x or 0X)
    int hex = 0X20; // Equivalent to 20 in decimal
    printf("Hexadecimal: %d (Hex input: 0X20)\n", hex);
    printf("Hexadecimal: %d (Hex input: 0X22)\n", 0x22);

    // Using constants in expressions
    int sum = dec + 010 + 0xA; // Adding decimal, octal, and hex constants
    printf("Sum (20 + 010 + 0xA): %d\n", sum);

    // Non-decimal constants in a print statement
    printf("Octal in printf: %o, Hexadecimal in printf: %x\n", oct, hex);

    return 0;
}