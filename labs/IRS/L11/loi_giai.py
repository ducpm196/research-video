import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
mmr = lambda r, s: kv['lam'] * r - (1.0 - kv['lam']) * s
sx, sy = mmr(kv['rx'], kv['sx']), mmr(kv['ry'], kv['sy'])
print(f'mmr_X={sx:.3f} mmr_Y={sy:.3f} pick={"Y" if sy > sx else "X"}')
