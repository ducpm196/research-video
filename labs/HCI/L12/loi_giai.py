wcag1 = sum([16, 30, 19])
contrast = (0.90 + 0.05) / (0.05 + 0.05)
area_24 = 24 * 24
ratio = (48 * 48) / area_24
print(f"wcag1={wcag1} contrast_ratio={contrast:.1f} area_24={area_24} ratio_48_24={ratio:.2f}x")
