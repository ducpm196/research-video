import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
rat = kv['gft'] / kv['cdc']; err = (kv['gft'] - kv['cdc']) / kv['cdc'] * 100
print(f'ratio={rat:.2f}x rel_err_pct={err:.1f}%')
