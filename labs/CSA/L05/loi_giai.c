#include <stdio.h>
static int nand_g(int a, int b) { return !(a & b); }
static int g_not(int a) { return nand_g(a, a); }
static int g_and(int a, int b) { return g_not(nand_g(a, b)); }
static int g_or(int a, int b) { return nand_g(g_not(a), g_not(b)); }
static int g_xor(int a, int b) { int t = nand_g(a, b); return nand_g(nand_g(a, t), nand_g(b, t)); }
int main(void) {
    int a1=1, b1=1, c1=1, a2=1, b2=0, c2=1;
    if (scanf("a1=%d b1=%d c1=%d a2=%d b2=%d c2=%d", &a1, &b1, &c1, &a2, &b2, &c2) != 6) return 1;
    printf("not1=%d and11=%d or01=%d xor11=%d\n", g_not(1), g_and(1,1), g_or(0,1), g_xor(1,1));
    int s1 = g_xor(g_xor(a1,b1),c1), co1 = g_or(g_and(a1,b1), g_and(c1, g_xor(a1,b1)));
    int s2 = g_xor(g_xor(a2,b2),c2), co2 = g_or(g_and(a2,b2), g_and(c2, g_xor(a2,b2)));
    printf("fa_111_sum=%d fa_111_cout=%d\n", s1, co1);
    printf("fa_101_sum=%d fa_101_cout=%d\n", s2, co2);
    return 0;
}
