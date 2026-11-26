import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
deploys, days = int(kv['deploys']), int(kv['days'])
ts = sorted(int(v) for v in kv['leads'].split(','))
med = ts[len(ts) // 2]; avg = sum(ts) / len(ts)
print(f'deploy_per_day={deploys / days:.2f}')
print(f'lead_median_h={med}')
print(f'lead_mean_h={avg:.1f}')
