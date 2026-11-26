#include <stdio.h>
static void swap_ptr(int *a, int *b) {
    if (!a || !b) return;
    int t = *a; *a = *b; *b = t;
}
static void divmod_i(int x, int d, int *q, int *r) {
    if (q) *q = x / d;
    if (r) *r = x % d;
}
int main(void) {
    int x = 42, y = 99, q = 0, r = 0;
    swap_ptr(&x, &y);
    divmod_i(47, 5, &q, &r);
    printf("swap: x=%d y=%d\n", x, y);
    printf("divmod: q=%d r=%d\n", q, r);
    return 0;
}
