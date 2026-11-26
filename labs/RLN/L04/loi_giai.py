import sys
s = sys.stdin.read().strip() or "3.0,6.0,9.0|5.0 2.0 8.0 0.9 0.25"
ms, ts = s.split("|")
mcv = [float(x) for x in ms.split(",")]
V, r, Vn, g, a = map(float, ts.split())
mc = sum(mcv) / len(mcv)
td = V + a * (r + g * Vn - V)
print(f"MC={mc:.1f} TD0={td:.2f}")
