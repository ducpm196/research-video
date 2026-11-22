u, v = 0.25, 0.5
top = (1 - u) * 10 + u * 30
bot = (1 - u) * 50 + u * 70
bilerp = (1 - v) * top + v * bot
levels = len([512 >> k for k in range(10)])
ratios = sum(0.25 ** k for k in range(1, 10))
print(f"bilerp={bilerp:.1f} levels={levels} mip_extra_ratio={ratios:.3f}")
