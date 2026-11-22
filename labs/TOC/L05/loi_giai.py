tr = [(1, 2), (1, 2), (2, 1), (4, 4), (4, 3)]
acc, reach, q = {2, 4}, {0}, [0]
while q:
    for v in tr[q.pop(0)]:
        if v not in reach: reach.add(v); q.append(v)
st = sorted(reach); prs = [(u, v) for u in st for v in st if u < v]
dist = {(u, v) for u, v in prs if (u in acc) != (v in acc)}
pair = lambda a, b: (a, b) if a < b else (b, a)
for _ in st:
    dist |= {(u, v) for u, v in prs
             if any(pair(tr[u][a], tr[v][a]) in dist for a in (0, 1))}
cls = {tuple(v for v in st if pair(u, v) not in dist) for u in st}
print(f"reachable={len(st)} marked_pairs={len(dist)}",
      f"min_dfa_states={len(cls)}")
