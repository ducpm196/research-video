p3 = 2 / 3
for t in range(4, 11): p3 *= (t - 1) / t
p10 = 2 / 10
print(f'exact_prob_p3={p3:.3f}')
print(f'exact_prob_p10={p10:.3f}')
print(f'uniform_verified={int(abs(p3 - p10) < 1e-12)}')
