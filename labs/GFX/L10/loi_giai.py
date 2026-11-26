import sys
s = sys.stdin.read().strip() or "0.04|1.0,0.5,0.1"
fs, cs = s.split("|")
F0 = float(fs); c0, c1, c2 = map(float, cs.split(","))
schlick = lambda cos_t: F0 + (1.0 - F0) * ((1.0 - cos_t) ** 5)
print(f"F0={schlick(c0):.3f} F60={schlick(c1):.3f} F84={schlick(c2):.3f}")
