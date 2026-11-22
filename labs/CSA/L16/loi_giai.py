s8 = 1.0 / (0.15 + 0.85 / 8.0)
lim = 1.0 / 0.15
print(f'speedup_8cores_p85={s8:.2f}')
print(f'limit_inf={lim:.2f}')
print(f'cache_timing_ratio={100.0 / 2.0:.1f}x')
