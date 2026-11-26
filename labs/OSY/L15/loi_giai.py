import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
checks = kv['procs'] * kv['hz']
w1, w2 = kv['w1'], kv['w2']; tot = w1 + w2
ran, v, first = {'A': 0, 'B': 0}, {'A': 0, 'B': 0}, None
slices = {'A': kv['s1'], 'B': kv['s2']}
while sum(ran.values()) < kv['total_ms']:
    elig = [k for k in ('A', 'B') if 2 * v[k] <= v['A'] + v['B']]
    pick = min(elig, key=lambda k: (v[k] + slices[k], 0 if k == 'A' else 1))
    if first is None:
        first = pick
    d = min(slices[pick], kv['total_ms'] - sum(ran.values()))
    ran[pick] += d; v[pick] += d
print(f'on_checks_per_sec={checks}')
print(f'cfs_share_2048_vs_1024={100*w1/tot:.1f}%,{100*w2/tot:.1f}%')
print(f'eevdf_ms_36ms={ran["A"]},{ran["B"]} first={first}')
