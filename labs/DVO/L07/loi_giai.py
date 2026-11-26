import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n, p, obs = int(kv['n']), float(kv['p']), int(kv['obs'])
tail = sum(math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in range(obs, n + 1))
print(f'expected_errors={int(n * p)}')
print(f'tail_prob_ge20={tail:.4f}')
print(f'rollback_triggered={int(tail < 0.01)}')
