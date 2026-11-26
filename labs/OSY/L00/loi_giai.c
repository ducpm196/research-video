#include <stdio.h>
int main(void) {
    double r1=1000.0, r2=50000.0, us=5.0; int sw=1;
    if (scanf("r1=%lf r2=%lf ctx_us=%lf is_sys=%d", &r1, &r2, &us, &sw) != 4) return 1;
    printf("cpu_pct_1k=%.2f\n", r1 * us * 1e-6 * 100.0);
    printf("cpu_pct_50k=%.2f\n", r2 * us * 1e-6 * 100.0);
    printf("syscall_mode_switch=%d\n", sw ? 1 : 0);
    return 0;
}
