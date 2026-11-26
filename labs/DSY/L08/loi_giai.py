import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
ts = [float(kv['fast_s'])] * int(kv['fast_cnt']) + [float(kv['slow_s'])]
mn = sum(ts) / len(ts); mx = int(max(ts))
print(f'mean_s={mn:.1f}')
print(f'job_done_s={mx}')
print(f'straggler_ratio={mx / mn:.1f}x')
