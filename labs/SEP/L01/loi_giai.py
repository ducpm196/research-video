combos = 365 * 50 * 2
p_unique = (1.0 - 1.0 / combos) ** (8000 - 1)
print(f"combos={combos} prob_unique={p_unique:.3f}")
