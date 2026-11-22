p = 0.75
pass_at_4 = (1.0 - (1.0 - p) ** 4) * 100
pass_pow_4 = (p ** 4) * 100
print(f"pass_at_4={pass_at_4:.1f}% pass_pow_4={pass_pow_4:.1f}%")
