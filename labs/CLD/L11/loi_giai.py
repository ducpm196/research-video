import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
af = (1.0 - float(kv['p_slow'])) ** int(kv['k'])
print(f'all_fast_pct={af * 100:.1f}%\nslow_req_pct={(1.0 - af) * 100:.1f}%')
