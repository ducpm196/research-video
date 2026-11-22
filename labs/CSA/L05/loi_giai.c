#include <stdio.h>
static int nand_g(int a, int b) { return !(a & b); }
static int g_not(int a) { return nand_g(a, a); }
static int g_and(int a, int b) { return g_not(nand_g(a, b)); }
static int g_or(int a, int b) { return nand_g(g_not(a), g_not(b)); }
static int g_xor(int a, int b) { int t = nand_g(a, b); return nand_g(nand_g(a, t), nand_g(b, t)); }
int main(void) {
    printf("not1=%d and11=%d or01=%d xor11=%d\n", g_not(1), g_and(1,1), g_or(0,1), g_xor(1,1));
    int s1 = g_xor(g_xor(1,1),1), c1 = g_or(g_and(1,1), g_and(1, g_xor(1,1)));
    int s2 = g_xor(g_xor(1,0),1), c2 = g_or(g_and(1,0), g_and(1, g_xor(1,0)));
    printf("fa_111_sum=%d fa_111_cout=%d\n", s1, c1);
    printf("fa_101_sum=%d fa_101_cout=%d\n", s2, c2);
    return 0;
}
