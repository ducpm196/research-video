import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
be = round(kv['reserved'] / kv['hourly']); pct = 100.0 * be / 8760; sv = round(8760 * kv['hourly'] - kv['reserved'])
print(f'breakeven_hours={be}\nbreakeven_pct_year={pct:.1f}%\nfull_year_saved_usd={sv}')
