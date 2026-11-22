tp, fp, fn = 4, 1, 2
p = tp / (tp + fp); r = tp / (tp + fn); f1 = 2 * p * r / (p + r)
ece = 0.5 * abs(0.80 - 0.90) + 0.5 * abs(0.40 - 0.60)
print(f'precision={p:.2f} recall={r:.2f}')
print(f'f1={f1:.2f}')
print(f'ece={ece:.2f}')
