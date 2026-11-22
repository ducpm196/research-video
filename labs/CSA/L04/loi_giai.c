#include <stdio.h>
#include <float.h>
int main(void) {
    double big = 1e16;
    printf("left_assoc=%.1f\n", (big + 1.0) - big);
    printf("right_assoc=%.1f\n", 1.0 + (big - big));
    printf("eps_f32_lt_1e6=%d\n", FLT_EPSILON < 1e-6f ? 1 : 0);
    return 0;
}
