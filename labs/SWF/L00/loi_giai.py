import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
arr = [int(v) for v in kv['arr'].split(',')]
bad = [int(v) for v in kv['bad'].split(',')]
def bs(a, x):
    if any(a[i] > a[i + 1] for i in range(len(a) - 1)):
        return None
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        m = lo + (hi - lo) // 2
        if a[m] == x:
            return m
        if a[m] < x:
            lo = m + 1
        else:
            hi = m - 1
    return -1
rej = int(bs(bad, bad[0]) is None)
print(f'found_idx={bs(arr, int(kv["x_hit"]))}')
print(f'missing_idx={bs(arr, int(kv["x_miss"]))}')
print(f'unsorted_rejected={rej}')
