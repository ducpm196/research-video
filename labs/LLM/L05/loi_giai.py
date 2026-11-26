import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
b = 2 * kv['layers'] * kv['hidden'] * kv['ctx'] * kv['bytes']
print(f'kv_bytes={b} kv_GiB={b / (1024 ** 3):.1f}')
