import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
rd = (kv['b'] - kv['a']) / kv['a'] * 100; vr = (kv['b'] - kv['base']) / (kv['a'] - kv['base'])
print(f'real_diff_pct={rd:.1f}% visual_ratio={vr:.1f}x')
