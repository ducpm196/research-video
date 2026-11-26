#include <stdio.h>
#include <string.h>
int main(void) {
    size_t cap = 0;
    char src[128] = {0}, buf[64] = {0};
    if (scanf("%zu %127s", &cap, src) != 2 || cap == 0 || cap > 64) return 1;
    snprintf(buf, cap, "%s", src);
    size_t blen = strlen(buf);
    printf("src_len=%zu buf_size=%zu\n", strlen(src), cap);
    printf("cut=%s last_byte=%d\n", buf, (int)(unsigned char)buf[blen]);
    return 0;
}
