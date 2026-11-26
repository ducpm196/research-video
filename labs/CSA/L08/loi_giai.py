import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
ic = float(kv['ic']); hz_a = float(kv['hz_a']); hz_b = float(kv['hz_b']); cpi_b = float(kv['cpi_b'])
cpi = sum(float(f)*float(c) for p in kv['mix'].split(',') for f,c in [p.split(':')])
t_a = ic * cpi / hz_a; t_b = ic * cpi_b / hz_b
print(f'cpi_avg={cpi:.2f}')
print(f'cpu_time_s={t_a:.3f}')
print(f'speedup_vs_3ghz_cpi3={t_b / t_a:.2f}')
