import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
avg = (kv['dau'] * kv['req_day']) / 86400; peak = avg * kv['peak_x']; mb = (peak * kv['req_b']) / 1e6
print(f'avg_qps={round(avg)}\npeak_qps={round(peak)}\npeak_mb_per_s={mb:.2f}')
