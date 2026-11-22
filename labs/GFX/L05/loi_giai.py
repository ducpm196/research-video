dz_mm = lambda z, n, f=2000.0, bits=24: (z*z*(f - n)) / (f * n * (1 << bits)) * 1000.0
d1, d2 = dz_mm(200.0, 0.1), dz_mm(200.0, 1.0)
print(f"dz_n01_mm={d1:.2f} dz_n10_mm={d2:.2f} gain={d1/d2:.1f}x")
