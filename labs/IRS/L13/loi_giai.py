import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
mb = int(kv['videos']) * int(kv['dim']) * 4 / (1024 ** 2)
vpu = float(kv['views_m']) / float(kv['users_m']); lc = -math.log(float(kv['q']))
print(f'emb_mib={mb:.1f} views_u={vpu:.1f} log_corr={lc:.3f}')
