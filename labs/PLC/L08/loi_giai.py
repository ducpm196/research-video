adj = {'R': ['A'], 'A': ['B'], 'B': [], 'C': ['D'], 'D': ['C'], 'E': []}
alive = {'R'}; q = ['R']
while q:
    u = q.pop(0)
    for v in adj[u]:
        if v not in alive:
            alive.add(v); q.append(v)
reclaimed = sorted(set(adj) - alive)
print(f"alive={sorted(alive)} reclaimed={reclaimed}")
