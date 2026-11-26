import sys
s = sys.stdin.read().strip() or "365 50 2 8000"
ds, ags, gs, ps = s.split()
combos = int(ds) * int(ags) * int(gs)
p_unique = (1.0 - 1.0 / combos) ** (int(ps) - 1)
print(f"combos={combos} prob_unique={p_unique:.3f}")
