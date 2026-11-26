import math, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
lo, hi = 0, kv['n2'] - 1
while lo < hi:
    m = (lo + hi) // 2
    if m >= kv['bad']: hi = m
    else: lo = m + 1
print(f'bisect_steps_3={math.ceil(math.log2(kv["n1"]))}')
print(f'bisect_steps_300={math.ceil(math.log2(kv["n2"]))}')
print(f'found_bad_commit={lo}')
