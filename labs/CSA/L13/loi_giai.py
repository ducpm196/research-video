import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
p = kv['p']; amd = lambda n: 1.0 / ((1.0 - p) + p / n)
print(f'speedup_4={amd(int(kv["n1"])):.2f}')
print(f'speedup_16={amd(int(kv["n2"])):.2f}')
print(f'max_limit={1.0 / (1.0 - p):.2f}')
