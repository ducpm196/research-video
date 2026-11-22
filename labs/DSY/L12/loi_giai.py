src = ['VN']*6 + ['US']*3 + ['VN']; runs = []
for x in src:
    if runs and runs[-1][0] == x: runs[-1][1] += 1
    else: runs.append([x, 1])
dec = [v for v, c in runs for _ in range(c)]
print(f'col_scan_pct={100 / 8:.1f}%')
print(f'rle_runs={len(runs)}')
print(f'rle_roundtrip_ok={int(dec == src)}')
