import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
g1 = round(kv['calls'] * (kv['ms1'] / 1000.0) * kv['mem1']); g2 = round(kv['calls'] * (kv['ms2'] / 1000.0) * kv['mem2'])
print(f'gb_sec_512mb={g1}\ngb_sec_1gb={g2}\nsame_gb_sec={int(g1 == g2)}')
