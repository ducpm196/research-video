import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
lo, hi, mx = kv['lo'], kv['hi'], kv['max32']
mid = lo + (hi - lo) // 2
print(f'naive_sum_overflows={int(lo + hi > mx)}')
print(f'safe_mid={mid}')
print(f'in_bounds={int(lo <= mid <= hi)}')
