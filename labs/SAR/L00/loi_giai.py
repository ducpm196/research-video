import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
lats = sorted(kv['base'] + (i % kv['mod']) * kv['step'] for i in range(100))
p95, p99 = lats[94], lats[98]
print(f'p95_ms={p95}\np99_ms={p99}\nslo_pass={int(p95 <= kv["slo"])}')
