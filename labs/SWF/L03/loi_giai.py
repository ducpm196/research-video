lo, hi, mx = 2_000_000_000, 2_100_000_000, (1 << 31) - 1
mid = lo + (hi - lo) // 2
print(f'naive_sum_overflows={int(lo + hi > mx)}')
print(f'safe_mid={mid}')
print(f'in_bounds={int(lo <= mid <= hi)}')
