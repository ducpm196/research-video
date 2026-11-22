from collections import deque
g = {
    'S': ['A', 'B'], 'A': ['C', 'D'],
    'B': ['G'], 'C': ['G'], 'D': [], 'G': [],
}
q, seen, expanded, found_d = deque([('S', 0)]), {'S'}, 0, -1
while q and found_d < 0:
    u, d = q.popleft()
    expanded += 1
    for v in g[u]:
        if v not in seen:
            seen.add(v)
            if v == 'G': found_d = d + 1; break
            q.append((v, d + 1))
print(f"shortest={found_d} expanded={expanded} visited={len(seen)}")
