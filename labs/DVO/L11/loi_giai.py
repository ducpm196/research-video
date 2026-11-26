import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
b_day = kv['rps'] * kv['rec_B'] * 86400
gb = b_day / 1e9
tb = (b_day * kv['days']) / 1e12
print(f'gb_per_day={gb:.1f}')
print(f'tb_30_days={tb:.2f}')
print(f'sampling_10pct_tb={tb * kv["sample_pct"]:.2f}')
