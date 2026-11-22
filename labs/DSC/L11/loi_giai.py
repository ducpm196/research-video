n, prev, sens, spec = 10000, 0.02, 0.95, 0.90
tp = n * prev * sens
fp = n * (1.0 - prev) * (1.0 - spec)
ppv = tp / (tp + fp)
print(f"tp={tp:.1f} fp={fp:.1f} ppv={ppv:.3f}")
