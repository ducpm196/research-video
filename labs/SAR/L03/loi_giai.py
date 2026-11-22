RANK = {'UI': 0, 'App': 1, 'Data': 2}
edges = [('UI', 'App'), ('App', 'Data'), ('UI', 'Data'), ('Data', 'App')]
ok = sum(RANK[u] < RANK[v] for u, v in edges)
bad = len(edges) - ok
print(f'valid_edges={ok}')
print(f'violations={bad}')
print(f'arch_clean={int(bad == 0)}')
