ppo = lambda rho, A, e=0.2: min(rho * A, max(1 - e, min(1 + e, rho)) * A)
print(f"pos_clipped={ppo(1.4, 3.0):.1f} neg_unclipped={ppo(0.6, -3.0):.1f}")
