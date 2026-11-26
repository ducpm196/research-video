import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
g, n, r = float(kv['gen']), float(kv['net']), float(kv['rank'])
t1 = g + n + int(kv['c1']) * r; t2 = g + n + int(kv['c2']) * r
tail = (1.0 - (1.0 - float(kv['p_slow'])) ** int(kv['shards'])) * 100
print(f'p99_before={t1:.0f}ms p99_after={t2:.0f}ms tail8={tail:.1f}%')
