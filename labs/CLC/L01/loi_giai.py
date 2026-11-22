p = 0.01
a2 = 1.0 - p ** 2
a3 = 1.0 - p ** 3
dt = (1.0 - a2) * 525600
print(f'az2_avail_pct={100 * a2:.4f}%')
print(f'az3_avail_pct={100 * a3:.4f}%')
print(f'az2_downtime_min_year={dt:.1f}')
