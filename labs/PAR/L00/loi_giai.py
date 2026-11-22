p = 0.80
s8 = 1.0 / ((1.0 - p) + p / 8.0)
s_inf = 1.0 / (1.0 - p)
print(f"amdahl_8={s8:.2f}x max_limit={s_inf:.1f}x")
