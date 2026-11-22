prev = 1 / 10000; tpr = 0.99; fpr = 0.01
tp = 1_000_000 * prev * tpr; fp = 1_000_000 * (1 - prev) * fpr
ppv = tp / (tp + fp)
print(f'tp_per_1m={round(tp)}')
print(f'fp_per_1m={round(fp)}')
print(f'ppv_pct={100 * ppv:.2f}%')
