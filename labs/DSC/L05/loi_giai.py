v0, v1, cut = 82.0, 84.0, 80.0
real_pct = (v1 - v0) / v0 * 100
fake_ratio = (v1 - cut) / (v0 - cut)
print(f"real_gain={real_pct:.2f}% truncated_visual={fake_ratio:.1f}x")
