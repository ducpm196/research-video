dz = lambda z, n, f=10000.0: (z*z*(f - n)) / (f * n * (1 << 24))
print(f"dz_n002={dz(1000.0, 0.02):.2f}m dz_n100={dz(1000.0, 1.00):.2f}m")
