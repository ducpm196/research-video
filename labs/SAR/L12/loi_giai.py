import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
wq = kv['monthly'] / (30 * 86400); rq = round(wq * kv['ratio'])
tb5 = (60 * kv['monthly'] * kv['rec_b']) / 1e12
print(f'write_qps={wq:.1f}\nread_qps={rq}\nstorage_5yr_tb={tb5:.1f}')
