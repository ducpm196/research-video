fwer = 1.0 - (1.0 - 0.05)**15
alpha_bonf = 0.05 / 15
fwer_bonf = 1.0 - (1.0 - alpha_bonf)**15
print(f"raw_fwer={fwer:.3f} bonf_alpha={alpha_bonf:.4f} fwer_bonf={fwer_bonf:.3f}")
