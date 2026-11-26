#include <stdio.h>
#include <stdint.h>
int main(void) {
    unsigned x = 47;
    printf("dec=%u hex=0x%02X\n", x, x);
    printf("u8_states=%d max=%u\n", 1 << 8, UINT8_MAX);
    printf("kib_minus_kb=%d\n", 1024 - 1000);
    return 0;
}
