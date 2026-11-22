#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef struct { uint64_t ts; uint16_t hdr; uint16_t flag; uint32_t amt; } Rec;
int main(void) {
    size_t cap = 2, len = 0;
    Rec *d = malloc(cap * sizeof(Rec)); if (!d) return 1;
    uint32_t amts[5] = {100, 250, 400, 150, 600};
    for (int i = 0; i < 5; i++) {
        if (len == cap) {
            size_t nc = cap * 2;
            if (nc > SIZE_MAX / sizeof(Rec)) { free(d); return 1; }
            Rec *t = realloc(d, nc * sizeof(Rec));
            if (!t) { free(d); return 1; }
            d = t; cap = nc;
        }
        uint16_t tp = (uint16_t)(i % 2 == 0 ? 1 : 2);
        d[len++] = (Rec){(uint64_t)(i + 1), (uint16_t)(tp << 12), 0, amts[i]};
    }
    uint64_t s1 = 0;
    for (size_t i = 0; i < len; i++) if (((d[i].hdr >> 12) & 0xF) == 1) s1 += d[i].amt;
    printf("rec_size=%zu cap=%zu sum_t1=%llu\n", sizeof(Rec), cap, (unsigned long long)s1);
    free(d); d = NULL;
    printf("clean=%d\n", d == NULL);
    return 0;
}
