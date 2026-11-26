#include <stdio.h>
static void swap_ptr(int *a, int *b) {
    if (!a || !b) return;
    int t = *a; *a = *b; *b = t;
}
static int divmod_i(int x, int d, int *q, int *r) {
    if (d == 0) return 0;
    if (q) *q = x / d;
    if (r) *r = x % d;
    return 1;
}
int main(void) {
    int x = 0, y = 0, num = 0, den = 0, q = 0, r = 0;
    if (scanf("%d %d %d %d", &x, &y, &num, &den) != 4) return 1;
    swap_ptr(&x, &y);
    printf("swap: x=%d y=%d\n", x, y);
    if (divmod_i(num, den, &q, &r)) printf("divmod: q=%d r=%d\n", q, r);
    else printf("divmod: ERR_ZERO\n");
    return 0;
}
