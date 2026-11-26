import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
t = int(kv['t'])
van = kv['rv'] ** t; exp = kv['re'] ** t
print(f"vanish_20={van:.5f} explode_20={exp:.2f}")
print(f"clipped_norm={min(exp, kv['clip']):.2f}")
