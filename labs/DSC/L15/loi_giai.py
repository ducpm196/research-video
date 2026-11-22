import math
goal = math.floor(0.9525 * 0.9 * 10000) / 10000
imp = (0.9525 - 0.8567) / 0.9525 * 100
mse_gap = round(2 * 800 / (2_817_131 / 2), 5)
opt = math.sqrt(0.8558**2 + mse_gap) - 0.8558
print(f"goal={goal:.4f} win_imp={imp:.2f}% blend_opt={opt:.5f}")
