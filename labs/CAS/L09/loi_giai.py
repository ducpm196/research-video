import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
def ok(p, r): return p >= 0 and (1 + 2 + p + 16) <= r
over = max(0, kv['p_bad'] - (kv['r_bad'] - 3))
print(f'valid_ok={int(ok(kv["p_ok"], kv["r_ok"]))} hb_ok={int(ok(kv["p_bad"], kv["r_bad"]))} hb_overread_B={over}')
