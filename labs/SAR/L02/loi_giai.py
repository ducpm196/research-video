avg = (4_000_000 * 30) / 86400
peak = avg * 3
mb_s = (peak * 1500) / 1e6
print(f'avg_qps={round(avg)}')
print(f'peak_qps={round(peak)}')
print(f'peak_mb_per_s={mb_s:.2f}')
