import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
tot = 10 ** kv['digits']
p1 = kv['tries'] / tot; p2 = kv['unbounded'] / tot
print(f'prob_3_tries={p1:.0e}')
print(f'prob_unbounded_500k={p2:.2f}')
print(f'rate_limit_factor={round(p2 / p1)}x')
