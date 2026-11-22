lats = sorted(60 + (i % 25) * 4 for i in range(100))
p95, p99 = lats[94], lats[98]
print(f'p95_ms={p95}')
print(f'p99_ms={p99}')
print(f'slo_pass={int(p95 <= 160)}')
