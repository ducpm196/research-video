combos = 2 * 5 * 365 * 100
p_uniq = (1.0 - 1.0 / combos) ** (50000 - 1)
fine_b = max(3.0, 200.0 * 0.05)
print(f"combos={combos} prob_unique={p_uniq:.3f} max_fine_B={fine_b:.1f}")
