#include <stdio.h>
#include <stdint.h>
int main(void) {
    unsigned x = 47, kib = 1;
    if (scanf("x=%u kib_count=%u", &x, &kib) != 2) return 1;
    printf("dec=%u hex=0x%02X\n", x, x);
    printf("u8_states=%d max=%u\n", 1 << 8, UINT8_MAX);
    printf("kib_minus_kb=%u\n", (1024U - 1000U) * kib);
    return 0;
}
