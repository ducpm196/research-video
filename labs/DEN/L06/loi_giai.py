g = {'u0': ['u1', 'u2'], 'u1': ['u2', 'u3'], 'u2': ['u3', 'u4'],
     'u3': ['u5'], 'u4': [], 'u5': []}
seen, frontier = {'u0'}, ['u0']
for _ in range(2):
    nxt = []
    for u in frontier:
        for v in g[u]:
            if v not in seen: seen.add(v); nxt.append(v)
    frontier = nxt
res = sorted(seen - {'u0'})
print(f'reached_sorted={res}')
print(f'unique_count={len(res)}')
