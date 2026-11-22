#include <stdio.h>
#include <stddef.h>
static int sum_ro(const int *a, size_t n) {
    int s = 0;
    for (size_t i = 0; i < n; i++) s += *(a + i);
    return s;
}
int main(void) {
    int v[5] = {2, 4, 6, 8, 10};
    ptrdiff_t d = (const char *)(v + 4) - (const char *)v;
    printf("offset4=%td\n", d);
    printf("sum=%d\n", sum_ro(v, 5));
    return 0;
}
