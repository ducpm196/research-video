import math, sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
print(f'ppl={math.exp(kv["loss"]):.2f} flops={6.0 * kv["params"] * kv["tokens"]:.2e}')
