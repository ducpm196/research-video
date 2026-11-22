N = 16
s_bad = 1.0 / (0.20 + 0.80 / N)
s_fix = 1.0 / (0.04 + 0.96 / N)
print(f"amdahl_before={s_bad:.2f}x amdahl_after={s_fix:.2f}x")
