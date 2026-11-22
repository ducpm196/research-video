#include <stdio.h>
int main(void) {
    double t_1k = 1000.0 * 5e-6 * 100.0;
    double t_50k = 50000.0 * 5e-6 * 100.0;
    printf("cpu_pct_1k=%.2f\n", t_1k);
    printf("cpu_pct_50k=%.2f\n", t_50k);
    printf("syscall_mode_switch=1\n");
    return 0;
}
