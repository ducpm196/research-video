a = 0.98
par = 1.0 - (1.0 - a) ** 2
ser = a * a
ratio = round((1.0 - ser) / (1.0 - par))
print(f'parallel_pct={100 * par:.2f}%')
print(f'series_pct={100 * ser:.2f}%')
print(f'downtime_ratio={ratio}x')
