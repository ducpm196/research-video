import math
p, n = 0.78, 800
me = 1.96 * math.sqrt(p * (1 - p) / n) * 100
print(f"acc={p * 100:.1f}% margin_pp={me:.2f}")
