import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
full = kv['days'] * kv['mb_day']; pruned = kv['query_days'] * kv['mb_day']
print(f'full_scan_mb={full}\npruned_scan_mb={pruned}\nsaved_pct={100 * (full - pruned) / full:.1f}%')
