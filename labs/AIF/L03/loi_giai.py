import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
lo, hi, tgt, d = kv['lo'], kv['hi'], kv['N'] + 1.0, int(kv['d'])
for _ in range(50):
    mid = (lo + hi) / 2.0
    if sum(mid ** k for k in range(d + 1)) < tgt: lo = mid
    else: hi = mid
print(f'b_star={mid:.4f} sum_val={sum(mid ** k for k in range(d + 1)):.2f}')
