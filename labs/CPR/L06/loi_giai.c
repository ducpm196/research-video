#include <stdio.h>
#include <stdlib.h>
int main(void) {
    int *p = calloc(3, sizeof(int));
    if (!p) return 1;
    p[0] = 10; p[1] = 20; p[2] = 30;
    int *tmp = realloc(p, 5 * sizeof(int));
    if (!tmp) { free(p); return 1; }
    p = tmp; p[3] = 40; p[4] = 50;
    int sum = 0; for (int i = 0; i < 5; i++) sum += p[i];
    printf("len=5 sum=%d\n", sum);
    free(p); p = NULL;
    printf("freed=%d\n", p == NULL);
    return 0;
}
