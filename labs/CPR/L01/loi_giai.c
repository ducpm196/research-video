#include <stdio.h>
#include <stdint.h>
static int safe_add32(int32_t a, int32_t b, int32_t *out) {
    if ((b > 0 && a > INT32_MAX - b) || (b < 0 && a < INT32_MIN - b)) return 0;
    *out = a + b;
    return 1;
}
int main(void) {
    unsigned int ui = 0, ua = 0;
    int32_t a1 = 0, b1 = 0, a2 = 0, b2 = 0, r1 = 0, r2 = 0;
    if (scanf("%u %u %d %d %d %d", &ui, &ua, &a1, &b1, &a2, &b2) != 6) return 1;
    uint8_t u = (uint8_t)(ui + ua);
    printf("wrap=%u\n", u);
    if (safe_add32(a1, b1, &r1)) printf("add1=%d\n", r1); else printf("add1=OVERFLOW\n");
    if (safe_add32(a2, b2, &r2)) printf("add2=%d\n", r2); else printf("add2=OVERFLOW\n");
    return 0;
}
