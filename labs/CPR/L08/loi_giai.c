#include <stdio.h>
#include <stdint.h>
typedef struct { uint64_t ts; uint16_t hdr; uint16_t flag; uint32_t amt; } Rec;
int main(void) {
    uint16_t pk = (uint16_t)((7 << 12) | 250);
    printf("packed=%u type=%u len=%u\n", pk, (pk >> 12) & 0xF, pk & 0xFFF);
    Rec a[4] = {{1, pk, 0, 100}, {2, pk, 1, 200}, {3, pk, 0, 300}, {4, pk, 1, 400}};
    FILE *f = fopen("out.bin", "wb"); if (!f) return 1;
    fwrite(a, sizeof(Rec), 4, f); fclose(f);
    Rec b[4]; f = fopen("out.bin", "rb"); if (!f) return 1;
    size_t nr = fread(b, sizeof(Rec), 4, f); fclose(f);
    printf("bytes=%zu count=%zu\n", nr * sizeof(Rec), nr);
    return 0;
}
