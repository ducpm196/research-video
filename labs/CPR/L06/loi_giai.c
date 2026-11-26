#include <stdio.h>
#include <stdlib.h>
int main(void) {
    size_t n1 = 0, n2 = 0;
    if (scanf("%zu", &n1) != 1 || n1 == 0) return 1;
    int *p = calloc(n1, sizeof(int));
    if (!p) return 1;
    for (size_t i = 0; i < n1; i++) if (scanf("%d", &p[i]) != 1) { free(p); return 1; }
    if (scanf("%zu", &n2) != 1) { free(p); return 1; }
    size_t tot = n1 + n2;
    int *tmp = realloc(p, (tot ? tot : 1) * sizeof(int));
    if (!tmp) { free(p); return 1; }
    p = tmp;
    for (size_t i = n1; i < tot; i++) if (scanf("%d", &p[i]) != 1) { free(p); return 1; }
    long long sum = 0;
    for (size_t i = 0; i < tot; i++) sum += p[i];
    printf("len=%zu sum=%lld\n", tot, sum);
    free(p); p = NULL;
    printf("freed=%d\n", p == NULL);
    return 0;
}
