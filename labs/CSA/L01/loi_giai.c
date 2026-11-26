#include <stdio.h>
#include <stdint.h>
#include <string.h>
int main(void) {
    unsigned raw_u = 0xFF, base_u = 127;
    if (scanf("raw_hex=%X base=%u", &raw_u, &base_u) != 2) return 1;
    uint8_t raw = (uint8_t)raw_u; int8_t s = 0; memcpy(&s, &raw, 1);
    uint8_t v = (uint8_t)(base_u + 1U);
    printf("u8=%u i8=%d\n", raw, (int)s);
    printf("i8_min=%d i8_max=%d\n", INT8_MIN, INT8_MAX);
    printf("u8_wrap_127_plus_1=%u\n", v);
    return 0;
}
