import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
dgb = (kv['daily'] * kv['bytes']) // 1_000_000_000
avg = kv['daily'] / 86400; pk = round(avg * kv['peak_x'])
print(f'daily_gb={dgb}\navg_and_peak_tps={round(avg)},{pk}\nyearly_tb={dgb * 365 / 1000:.1f}')
