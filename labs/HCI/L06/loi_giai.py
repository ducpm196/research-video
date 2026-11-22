cov = lambda n, lam=0.25: (1.0 - (1.0 - lam) ** n) * 100
print(f"n6_pct={cov(6):.1f}% n12_pct={cov(12):.1f}%")
