import sys
counts = [int(v) for v in sys.stdin.read().strip().split('=')[1].split(',')]
tot = sum(counts)
p = [c / tot for c in counts]
lam = [c / pk for c, pk in zip(counts, p)]
print(f"p={p} sum={sum(p):.1f}")
print(f"lambda={[round(x, 1) for x in lam]}")
print(f"lagrange_equal={int(len(set(round(x, 6) for x in lam)) == 1)}")
