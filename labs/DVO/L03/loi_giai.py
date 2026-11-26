import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n = int(kv['tests']); p1, p2 = float(kv['p1']), float(kv['p2'])
g = (1 - p1) ** n; f1 = 1 - g; f2 = 1 - (1 - p2) ** n
print(f'flaky_fail_pct_300={100 * f1:.1f}%')
print(f'flaky_fail_pct_p0005={100 * f2:.1f}%')
print(f'pipeline_always_green_pct={100 * g:.1f}%')
