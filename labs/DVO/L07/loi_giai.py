import math
n, p = 1000, 0.01
tail = sum(math.comb(n, k)*(p**k)*((1-p)**(n-k)) for k in range(20, 60))
print(f'expected_errors={int(n*p)}')
print(f'tail_prob_ge20={tail:.4f}')
print(f'rollback_triggered={int(tail < 0.01)}')
