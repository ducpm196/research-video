warp = 32; branches = [10, 12, 10]
eff = sum(branches) / (len(branches) * warp) * 100
print(f"warp_eff_diverged={eff:.0f}%")
