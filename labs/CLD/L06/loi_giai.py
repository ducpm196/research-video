import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
fit = int(kv['cap'] // kv['req']); w = (kv['cap'] - fit * kv['req']) / kv['cap'] * 100
print(f'pods_per_node={fit}\nstranded_pct={w:.1f}%')
