#include <stdio.h>
int main(void) {
    unsigned long long arr_len = 0, scale_n = 0;
    if (scanf("%llu %llu", &arr_len, &scale_n) != 2) return 1;
    printf("char=%zu int=%zu ll=%zu ptr=%zu\n", sizeof(char), sizeof(int), sizeof(long long), sizeof(void *));
    printf("arr_bytes=%zu\n", (size_t)arr_len * sizeof(int));
    printf("total_bytes=%llu\n", scale_n * (unsigned long long)sizeof(int));
    return 0;
}
