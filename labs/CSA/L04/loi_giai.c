#include <stdio.h>
#include <float.h>
int main(void) {
    double big = 1e16, delta = 1.0;
    if (scanf("big=%lf delta=%lf", &big, &delta) != 2) return 1;
    printf("left_assoc=%.1f\n", (big + delta) - big);
    printf("right_assoc=%.1f\n", delta + (big - big));
    printf("eps_f32_lt_1e6=%d\n", FLT_EPSILON < 1e-6f ? 1 : 0);
    return 0;
}
