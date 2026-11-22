b_day = 1000 * 1000 * 86400; gb = b_day / 1e9; tb30 = (b_day * 30) / 1e12
print(f'gb_per_day={gb:.1f}')
print(f'tb_30_days={tb30:.2f}')
print(f'sampling_10pct_tb={tb30 * 0.1:.2f}')
