T = 500
b0, b1 = 0.0002, 0.015
ab = 1.0
for t in range(T):
    beta = b0 + (b1 - b0) * t / (T - 1)
    ab *= (1.0 - beta)
print(f"alpha_bar_500={ab:.2e}")
print(f"noise_scale={(1.0 - ab) ** 0.5:.6f}")
