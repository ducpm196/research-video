ts = [10] * 99 + [300]; mn = sum(ts) / len(ts); mx = max(ts)
print(f'mean_s={mn:.1f}')
print(f'job_done_s={mx}')
print(f'straggler_ratio={mx / mn:.1f}x')
