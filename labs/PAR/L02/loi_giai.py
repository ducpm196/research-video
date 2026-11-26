import sys
s = sys.stdin.read().strip() or "511 9 16"
T1, Tinf, P = map(int, s.split())
lb = max(Tinf, T1 / P); ub = Tinf + (T1 - Tinf) / P
print(f"work={T1} span={Tinf} lower_bound={lb:.2f} brent_upper={ub:.2f}")
