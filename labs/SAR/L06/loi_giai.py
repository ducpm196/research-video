import sys
a = float(sys.stdin.read().split('=')[1])
par = 1.0 - (1.0 - a) ** 2; ser = a * a; rat = round((1.0 - ser) / (1.0 - par))
print(f'parallel_pct={100 * par:.2f}%\nseries_pct={100 * ser:.2f}%\ndowntime_ratio={rat}x')
