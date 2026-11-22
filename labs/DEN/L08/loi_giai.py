P, M = 10, 4
counts = [P // M + (1 if i < P % M else 0) for i in range(M)]
skew = (max(counts) - min(counts)) / min(counts) * 100
print(f'counts={counts}')
print(f'skew_pct={skew:.1f}%')
