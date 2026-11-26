import sys
s = sys.stdin.read().strip() or "500 50 1.0"
i1, i2, p2 = map(float, s.split())
p1 = 1.0 / i1
print(f"indep_leak={p1 * (1.0 / i2):.2e} shared_leak={p1 * p2:.2e}")
