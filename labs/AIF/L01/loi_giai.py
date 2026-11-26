import sys
from collections import deque, defaultdict
kv = dict(t.split('=') for t in sys.stdin.read().split())
g = defaultdict(list)
for item in kv['edges'].split(','):
    u, vs = item.split(':'); g[u] = [x for x in vs.split('|') if x]
s, goal = kv['start'], kv['goal']
fd = 0 if s == goal else -1
q, seen, exp = deque([(s, 0)]), {s}, 0
while q and fd < 0:
    u, d = q.popleft(); exp += 1
    for v in g[u]:
        if v not in seen:
            seen.add(v)
            if v == goal: fd = d + 1; break
            q.append((v, d + 1))
print(f'shortest={fd} expanded={exp} visited={len(seen)}')
