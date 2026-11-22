T1, Tinf, P = 511, 9, 16
lower_b = max(Tinf, T1 / P)
brent_upper = Tinf + (T1 - Tinf) / P
print(f"work={T1} span={Tinf} lower_bound={lower_b:.2f} brent_upper={brent_upper:.2f}")
