import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
low = (kv['low_min'] + kv['low_max']) // 2
elite = kv['elite_per_day'] * 365
print(f'low_per_year={low}')
print(f'elite_per_year={elite}')
print(f'ratio_round={round(elite / low)}x')
