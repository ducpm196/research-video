#include <stdio.h>
#include <stdint.h>
typedef struct { uint64_t ts; uint16_t hdr; uint16_t flag; uint32_t amt; } Rec;
int main(void) {
    unsigned int tp = 0, ln = 0;
    size_t cnt = 0;
    if (scanf("%u %u %zu", &tp, &ln, &cnt) != 3 || cnt == 0 || cnt > 128) return 1;
    uint16_t pk = (uint16_t)(((tp & 0xFU) << 12) | (ln & 0xFFFU));
    printf("packed=%u type=%u len=%u\n", pk, (pk >> 12) & 0xF, pk & 0xFFF);
    Rec a[128], b[128];
    for (size_t i = 0; i < cnt; i++) {
        uint32_t amt = 0;
        if (scanf("%u", &amt) != 1) return 1;
        a[i] = (Rec){(uint64_t)(i + 1), pk, (uint16_t)(i & 1U), amt};
    }
    FILE *f = fopen("out.bin", "wb"); if (!f) return 1;
    fwrite(a, sizeof(Rec), cnt, f); fclose(f);
    f = fopen("out.bin", "rb"); if (!f) return 1;
    size_t nr = fread(b, sizeof(Rec), cnt, f); fclose(f);
    unsigned long long sa = 0;
    for (size_t i = 0; i < nr; i++) sa += b[i].amt;
    printf("bytes=%zu count=%zu sum_amt=%llu\n", nr * sizeof(Rec), nr, sa);
    return 0;
}
