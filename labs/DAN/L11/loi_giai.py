a, b, base = 200.0, 212.0, 190.0
real_ratio = (b - a) / a * 100
visual_ratio = (b - base) / (a - base)
print(f"real_diff_pct={real_ratio:.1f}% visual_ratio={visual_ratio:.1f}x")
