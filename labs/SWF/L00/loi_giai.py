def bs(a, x):
    if any(a[i] > a[i+1] for i in range(len(a)-1)): raise ValueError('unsorted')
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        m = lo + (hi - lo) // 2
        if a[m] == x: return m
        if a[m] < x: lo = m + 1
        else: hi = m - 1
    return -1
rej = 0
try: bs([5, 2], 2)
except ValueError: rej = 1
print(f'found_idx={bs([2,5,8,12], 8)}')
print(f'missing_idx={bs([2,5,8,12], 7)}')
print(f'unsorted_rejected={rej}')
