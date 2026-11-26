import sys
s = sys.stdin.read().strip() or "2 5 365 100 50000 200.0"
g, r, d, y, n, rev = s.split()
combos = int(g) * int(r) * int(d) * int(y)
p_uniq = (1.0 - 1.0 / combos) ** (int(n) - 1)
fine_b = max(3.0, float(rev) * 0.05)
print(f"combos={combos} prob_unique={p_uniq:.3f} max_fine_B={fine_b:.1f}")
