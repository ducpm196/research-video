#include <stdio.h>
int main(void) {
    printf("char=%zu int=%zu ll=%zu ptr=%zu\n", sizeof(char), sizeof(int), sizeof(long long), sizeof(void *));
    int a[50];
    printf("arr50=%zu\n", sizeof(a));
    printf("total1M=%zu\n", (size_t)1000000 * sizeof(int));
    return 0;
}
