import sys
from collections import deque
kv = dict(t.split('=') for t in sys.stdin.read().split())
parse = lambda txt: dict(p.split(':') for p in txt.split(','))
s, g = parse(kv['init']), parse(kv['goal'])
st0 = tuple(sorted(s.items())); gt = tuple(sorted(g.items()))
q, seen, ans = deque([(st0, 0)]), {st0}, 0
while q:
    st, d = q.popleft()
    if st == gt: ans = d; break
    c = dict(st); clr = (set(c) - set(c.values())) | {'T'}
    for b in clr - {'T'}:
        for dst in clr - {b}:
            ks = tuple(sorted({**c, b: dst}.items()))
            if ks not in seen: seen.add(ks); q.append((ks, d + 1))
ib = [b for b, u in s.items() if u == 'T'][0]; gb = [b for b, u in g.items() if u == 'T'][0]
print(f'init_bottom={ib} goal_bottom={gb} min_actions={ans}')
