cpi = 0.50 * 1 + 0.30 * 3 + 0.20 * 2
t_a = 1e9 * cpi / 2e9
t_b = 1e9 * 3.0 / 3e9
print(f'cpi_avg={cpi:.2f}')
print(f'cpu_time_s={t_a:.3f}')
print(f'speedup_vs_3ghz_cpi3={t_b / t_a:.2f}')
