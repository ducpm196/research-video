import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
b, c, cap = kv['d_b'], kv['d_c'], kv['cap']; r = 0; hist = []
while min(b, c) < cap:
    r += 1
    if r % 2 == 1: b = min(cap, c + 1)
    else: c = min(cap, b + 1)
    hist.append((b, c))
print(f'after_round1=B:{hist[0][0]},C:{hist[0][1]}')
print(f'rounds_to_reach_16={r}')
print(f'final_vals={b},{c}')
