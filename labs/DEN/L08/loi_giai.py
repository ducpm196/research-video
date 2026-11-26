import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
P, M = kv['parts'], kv['members']
counts = [P // M + (1 if i < P % M else 0) for i in range(M)]
skew = (max(counts) - min(counts)) / min(counts) * 100
print(f'counts={counts}\nskew_pct={skew:.1f}%')
