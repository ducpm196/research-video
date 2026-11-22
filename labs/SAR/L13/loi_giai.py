daily_gb = (800_000_000 * 250) // 1_000_000_000
avg_tps = 800_000_000 / 86400
peak_tps = round(avg_tps * 3)
print(f'daily_gb={daily_gb}')
print(f'avg_and_peak_tps={round(avg_tps)},{peak_tps}')
print(f'yearly_tb={daily_gb * 365 / 1000:.1f}')
