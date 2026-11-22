#include <stdio.h>
static int is_pow2(unsigned n) { return n > 0 && (n & (n - 1)) == 0; }
int main(void) {
    unsigned x = 0x5A;
    printf("bit3=%u set0=0x%02X clr4=0x%02X\n", (x >> 3) & 1U, x | 1U, x & ~(1U << 4));
    printf("pow2_64=%d pow2_48=%d\n", is_pow2(64), is_pow2(48));
    printf("shift_mul=%u\n", 5U << 4);
    return 0;
}
