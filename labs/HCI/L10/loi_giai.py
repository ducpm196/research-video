p1 = 1.0 / 500.0
p2 = 1.0
p_indep = p1 * (1.0 / 50.0)
p_shared = p1 * p2
print(f"indep_leak={p_indep:.2e} shared_leak={p_shared:.2e}")
