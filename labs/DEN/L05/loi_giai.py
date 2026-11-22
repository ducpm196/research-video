days, per_day_mb, query_days = 30, 50, 2
full_mb = days * per_day_mb
pruned_mb = query_days * per_day_mb
print(f'full_scan_mb={full_mb}')
print(f'pruned_scan_mb={pruned_mb}')
print(f'saved_pct={100 * (full_mb - pruned_mb) / full_mb:.1f}%')
