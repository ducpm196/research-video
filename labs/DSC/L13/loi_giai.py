import sys
from collections import Counter
kv = dict(t.split('=') for t in sys.stdin.read().split())
rows = kv['rows'].split(','); mk = min(Counter(rows).values())
print(f'min_k={mk} is_2_anon={int(mk >= int(kv["k"]))}')
