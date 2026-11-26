import sys
from collections import Counter
kv = dict(t.split('=') for t in sys.stdin.read().split())
n, p, k = int(kv['events']), int(kv['parts']), kv['key']
raw = Counter([k] * n); salted = Counter(f'{k}#{i % p}' for i in range(n))
print(f'raw_hot_max={max(raw.values())}\nsalted_max={max(salted.values())}')
