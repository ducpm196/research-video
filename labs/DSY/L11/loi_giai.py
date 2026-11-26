import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
N, k = kv['N'], kv['k']
pk1 = k / (k + 1)
for t in range(k + 2, N + 1):
    pk1 *= (t - 1) / t
pN = k / N
print(f'exact_prob_p3={pk1:.3f}')
print(f'exact_prob_p10={pN:.3f}')
print(f'uniform_verified={int(abs(pk1 - pN) < 1e-12)}')
