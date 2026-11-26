import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
r = (kv['v1'] - kv['v0']) / kv['v0'] * 100; f = (kv['v1'] - kv['cut']) / (kv['v0'] - kv['cut'])
print(f'real_gain={r:.2f}% truncated_visual={f:.1f}x')
