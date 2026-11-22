av = lambda mtbf, mttr: 100 * mtbf / (mtbf + mttr)
print(f'avail_1h={av(720, 1.0):.3f}%')
print(f'avail_15m={av(720, 0.25):.3f}%')
print(f'downtime_cut_factor={1.0 / 0.25:.1f}x')
