#include <stdio.h>
#include <stdint.h>
#include <string.h>
int main(void) {
    uint8_t raw = 0xFF; int8_t s = 0; memcpy(&s, &raw, 1);
    printf("u8=%u i8=%d\n", raw, (int)s);
    printf("i8_min=%d i8_max=%d\n", INT8_MIN, INT8_MAX);
    uint8_t v = 127; v = (uint8_t)(v + 1);
    printf("u8_wrap_127_plus_1=%u\n", v);
    return 0;
}
