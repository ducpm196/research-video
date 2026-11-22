#include <stdio.h>
static void double_val(int x) { x = x * 2; (void)x; }
static int sum_to(int n) { return n <= 0 ? 0 : n + sum_to(n - 1); }
int main(void) {
    int v = 7;
    double_val(v);
    printf("after_call=%d\n", v);
    printf("sum8=%d stack_frames=%d\n", sum_to(8), 32 + 48 + 64);
    return 0;
}
