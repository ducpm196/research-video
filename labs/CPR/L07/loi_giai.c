#include <stdio.h>
#include <stdlib.h>
struct S1 { char a; int b; char c; };
struct S2 { int b; char a; char c; };
typedef struct Node { int v; struct Node *next; } Node;
int main(void) {
    printf("s1=%zu s2=%zu\n", sizeof(struct S1), sizeof(struct S2));
    Node *h = NULL;
    int vals[4] = {5, 10, 15, 20};
    for (int i = 0; i < 4; i++) {
        Node *n = malloc(sizeof(Node)); if (!n) return 1;
        n->v = vals[i]; n->next = h; h = n;
    }
    int s = 0, fr = 0;
    for (Node *c = h; c; c = c->next) s += c->v;
    while (h) { Node *nx = h->next; free(h); h = nx; fr++; }
    printf("list_sum=%d freed=%d\n", s, fr);
    return 0;
}
