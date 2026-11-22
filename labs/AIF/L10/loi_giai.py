from collections import deque
s = {'M': 'P', 'P': 'N', 'N': 'T'}; g = {'N': 'M', 'M': 'P', 'P': 'T'}
st0 = tuple(sorted(s.items()))
q, seen, ans = deque([(st0, 0)]), {st0}, 0
while q:
    c, d = dict(q[0][0]), q.popleft()[1]
    if c == g: ans = d; break
    clr = (set(c) - set(c.values())) | {'T'}
    for b in clr - {'T'}:
        for dst in clr - {b}:
            ks = tuple(sorted({**c, b: dst}.items()))
            if ks not in seen: seen.add(ks); q.append((ks, d + 1))
ib = [b for b, u in s.items() if u == 'T'][0]
gb = [b for b, u in g.items() if u == 'T'][0]
print(f"init_bottom={ib} goal_bottom={gb} min_actions={ans}")
