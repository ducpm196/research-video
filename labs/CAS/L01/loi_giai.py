import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
scale = 1 << int(kv['bits']); val = float(kv['val']); hz = int(kv['hz'])
err = val - int(val * scale) / scale
print(f'drift_50h={err * int(kv["h1"]) * 3600 * hz:.4f} drift_100h={err * int(kv["h2"]) * 3600 * hz:.4f}')
