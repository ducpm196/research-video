#include <stdio.h>
static void double_val(int x) { x = x * 2; (void)x; }
static long long sum_to(int n) { return n <= 0 ? 0 : (long long)n + sum_to(n - 1); }
int main(void) {
    int v = 0, n = 0, f1 = 0, f2 = 0, f3 = 0;
    if (scanf("%d %d %d %d %d", &v, &n, &f1, &f2, &f3) != 5) return 1;
    double_val(v);
    printf("after_call=%d\n", v);
    printf("sum=%lld stack_frames=%d\n", sum_to(n), f1 + f2 + f3);
    return 0;
}
