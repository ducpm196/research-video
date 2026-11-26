import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
f = kv['dim'] ** 2; lr = 2 * kv['dim'] * kv['r']
print(f'full={f} lora={lr} ratio={lr / f * 100:.2f}%')
