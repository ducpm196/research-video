import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
gb = int(kv['tb']) * 1024; cost = gb * float(kv['usd_gb']); sv = cost * float(kv['cdn_pct'])
print(f'egress_gb={gb}\nmonthly_usd={cost:.2f}\ncdn_saved_usd={sv:.2f}')
