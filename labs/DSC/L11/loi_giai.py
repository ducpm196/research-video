import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
tp = kv['n'] * kv['prev'] * kv['sens']; fp = kv['n'] * (1.0 - kv['prev']) * (1.0 - kv['spec'])
print(f'tp={tp:.1f} fp={fp:.1f} ppv={tp / (tp + fp):.3f}')
