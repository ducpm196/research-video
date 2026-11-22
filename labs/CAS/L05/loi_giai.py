rate_m = 460.0 / 45.0
prob_miss = 1.0 - (1.0 - 0.05) ** 8
print(f"loss_per_min_M={rate_m:.1f} prob_any_miss={prob_miss:.4f}")
