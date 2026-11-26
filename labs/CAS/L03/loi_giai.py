import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
act = kv['cmd'] * kv['lbf_to_n']
print(f'reported={kv["cmd"]:.1f} actual={act:.2f} factor={kv["lbf_to_n"]:.2f}')
