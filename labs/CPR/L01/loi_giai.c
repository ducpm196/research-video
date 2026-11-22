#include <stdio.h>
#include <stdint.h>
int main(void) {
    uint8_t u = (uint8_t)(250 + 10);
    printf("wrap=%u\n", u);
    int32_t a = 2147483640, b1 = 7, b2 = 8;
    if (a <= INT32_MAX - b1) printf("add1=%d\n", a + b1); else printf("add1=OVERFLOW\n");
    if (a <= INT32_MAX - b2) printf("add2=%d\n", a + b2); else printf("add2=OVERFLOW\n");
    return 0;
}
