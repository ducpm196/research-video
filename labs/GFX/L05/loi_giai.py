import sys
s = sys.stdin.read().strip() or "2000.0 200.0 24 0.1 1.0"
fs, zs, bs, n1s, n2s = s.split()
f, z, bits, n1, n2 = float(fs), float(zs), int(bs), float(n1s), float(n2s)
dz_mm = lambda n: (z*z*(f - n)) / (f * n * (1 << bits)) * 1000.0
d1, d2 = dz_mm(n1), dz_mm(n2)
print(f"dz_n01_mm={d1:.2f} dz_n10_mm={d2:.2f} gain={d1/d2:.1f}x")
