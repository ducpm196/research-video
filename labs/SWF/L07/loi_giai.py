import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
seq = [int(v) for v in kv['inord'].split(',')]
gh = [int(v) for v in kv['good_heap'].split(',')]
bh = [int(v) for v in kv['bad_heap'].split(',')]
b_ok = all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
def is_heap(h):
    return all(h[i] <= h[c] for i in range(len(h)) for c in (2 * i + 1, 2 * i + 2) if c < len(h))
print(f'bst_inorder_sorted={int(b_ok)}')
print(f'valid_heap={int(is_heap(gh))}')
print(f'broken_heap={int(is_heap(bh))}')
