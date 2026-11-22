p = 0.005
affected = int(500_000 * p)
prob_zero = (1.0 - p) ** 150
print(f"affected={affected} prob_zero_150={prob_zero:.3f}")
