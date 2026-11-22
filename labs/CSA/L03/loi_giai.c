#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
int main(void) {
    float f = -6.5f; uint32_t u = 0; memcpy(&u, &f, 4);
    int sign = (int)(u >> 31); int exp = (int)((u >> 23) & 0xFF) - 127;
    uint32_t mant = u & 0x7FFFFFU;
    printf("sign=%d exp_unbiased=%d mant_hex=0x%06X\n", sign, exp, mant);
    printf("close_03=%d\n", fabs((0.1 + 0.2) - 0.3) < 1e-9 ? 1 : 0);
    printf("hex32=0x%08X\n", u);
    return 0;
}
