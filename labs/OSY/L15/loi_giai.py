checks = 1000 * 1000
w1, w2 = 2048, 1024; tot = w1 + w2
ran, v, first = {'A': 0, 'B': 0}, {'A': 0, 'B': 0}, None
slices = {'A': 3, 'B': 9}
while sum(ran.values()) < 36:
    pick = 'A' if (v['A'] + slices['A']) <= (v['B'] + slices['B']) else 'B'
    if first is None: first = pick
    d = min(slices[pick], 36 - sum(ran.values()))
    ran[pick] += d; v[pick] += d
print(f'on_checks_per_sec={checks}')
print(f'cfs_share_2048_vs_1024={100*w1/tot:.1f}%,{100*w2/tot:.1f}%')
print(f'eevdf_ms_36ms={ran["A"]},{ran["B"]} first={first}')
