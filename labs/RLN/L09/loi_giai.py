import sys
s = sys.stdin.read().strip() or "0.2 1.4 3.0 0.6 -3.0"
e, r1, a1, r2, a2 = map(float, s.split())
ppo = lambda rho, A: min(rho * A, max(1 - e, min(1 + e, rho)) * A)
print(f"pos_clipped={ppo(r1, a1):.1f} neg_unclipped={ppo(r2, a2):.1f}")
