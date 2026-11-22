exp_a = 0.002 * 500_000
exp_b = 0.05 * 2_000
p_fleet = 1.0 - (1.0 - 0.002) ** 500
print(f"exp_A={exp_a:.0f} exp_B={exp_b:.0f} fleet_prob={p_fleet:.4f}")
