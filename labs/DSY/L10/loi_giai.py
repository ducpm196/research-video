import hashlib, math
m, n, k = 1000, 100, 7; bits = [0] * m
idx = lambda x, i: int(hashlib.sha256(f'{i}:{x}'.encode()).hexdigest(), 16) % m
for x in range(n):
    for i in range(k): bits[idx(x, i)] = 1
fn = sum(not all(bits[idx(x, i)] for i in range(k)) for x in range(n))
fpr = (1 - math.exp(-k * n / m)) ** k
print(f'false_negatives={fn}')
print(f'theory_fpr_pct={100*fpr:.2f}%')
print(f'bits_per_elem={m//n}')
