import sys
s = sys.stdin.read().strip() or "0.25 6 12"
ls, n1s, n2s = s.split()
lam, n1, n2 = float(ls), int(n1s), int(n2s)
cov = lambda n: (1.0 - (1.0 - lam) ** n) * 100.0
print(f"n6_pct={cov(n1):.1f}% n12_pct={cov(n2):.1f}%")
