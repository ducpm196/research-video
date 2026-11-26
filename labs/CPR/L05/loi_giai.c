#include <stdio.h>
#include <stddef.h>
static long long sum_ro(const int *a, size_t n) {
    long long s = 0;
    for (size_t i = 0; i < n; i++) s += *(a + i);
    return s;
}
int main(void) {
    size_t idx = 0, n = 0;
    int v[256] = {0};
    if (scanf("%zu %zu", &idx, &n) != 2 || n == 0 || n > 256 || idx >= n) return 1;
    for (size_t i = 0; i < n; i++) if (scanf("%d", &v[i]) != 1) return 1;
    ptrdiff_t d = (const char *)(v + idx) - (const char *)v;
    printf("offset=%td\n", d);
    printf("sum=%lld\n", sum_ro(v, n));
    return 0;
}
