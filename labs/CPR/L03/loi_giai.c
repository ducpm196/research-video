#include <stdio.h>
#include <string.h>
static int cut_copy(char *dst, size_t cap, const char *s) {
    return snprintf(dst, cap, "%s", s);
}
int main(void) {
    const char src[] = "BANKING_2026";
    char buf[8];
    int need = cut_copy(buf, sizeof(buf), src); (void)need;
    printf("src_len=%zu buf_size=%zu\n", strlen(src), sizeof(buf));
    printf("cut=%s last_byte=%d\n", buf, (int)buf[7]);
    return 0;
}
