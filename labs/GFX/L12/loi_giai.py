import sys
s = sys.stdin.read().strip() or "1000.0 10000.0 0.02 1.00"
z, f, n1, n2 = map(float, s.split())
dz = lambda n: (z*z*(f - n)) / (f * n * (1 << 24))
print(f"dz_n002={dz(n1):.2f}m dz_n100={dz(n2):.2f}m")
