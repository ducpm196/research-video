import math
p_raw = 2.0 / (200.0 + 2.0)
p_pow = (2.0 ** 0.75) / (200.0 ** 0.75 + 2.0 ** 0.75)
corr = -math.log(0.01)
print(f"raw_B={p_raw:.3f} pow075_B={p_pow:.3f} logq_corr={corr:.3f}")
