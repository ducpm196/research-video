import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
print(f'w_at_150={1000.0 / (kv["mu"] - kv["l1"]):.1f}ms')
print(f'w_at_190={1000.0 / (kv["mu"] - kv["l2"]):.1f}ms')
