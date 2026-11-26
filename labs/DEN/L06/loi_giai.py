import sys
from collections import defaultdict
kv = dict(t.split('=') for t in sys.stdin.read().split())
g = defaultdict(list)
for e in kv['edges'].split(','):
    u, v = e.split(':'); g[u].append(v)
st = kv['start']; seen, front = {st}, [st]
for _ in range(int(kv['hops'])):
    nxt = []
    for u in front:
        for v in g[u]:
            if v not in seen: seen.add(v); nxt.append(v)
    front = nxt
res = sorted(seen - {st})
print(f'reached_sorted={res}\nunique_count={len(res)}')
