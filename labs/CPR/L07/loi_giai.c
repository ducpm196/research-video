#include <stdio.h>
#include <stdlib.h>
struct S1 { char a; int b; char c; };
struct S2 { int b; char a; char c; };
typedef struct Node { int v; struct Node *next; } Node;
int main(void) {
    size_t n = 0;
    if (scanf("%zu", &n) != 1) return 1;
    printf("s1=%zu s2=%zu\n", sizeof(struct S1), sizeof(struct S2));
    Node *h = NULL;
    for (size_t i = 0; i < n; i++) {
        int val = 0;
        if (scanf("%d", &val) != 1) return 1;
        Node *nd = malloc(sizeof(Node)); if (!nd) return 1;
        nd->v = val; nd->next = h; h = nd;
    }
    long long s = 0; size_t fr = 0;
    for (Node *c = h; c; c = c->next) s += c->v;
    while (h) { Node *nx = h->next; free(h); h = nx; fr++; }
    printf("list_sum=%lld freed=%zu\n", s, fr);
    return 0;
}
