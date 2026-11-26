import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
o = (kv['maj_ok'] + kv['min_ok']) / (kv['maj_n'] + kv['min_n']) * 100
mj = kv['maj_ok'] / kv['maj_n'] * 100; mn = kv['min_ok'] / kv['min_n'] * 100
print(f'overall={o:.1f}% maj={mj:.1f}% min={mn:.1f}%')
