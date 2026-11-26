import sys
RANK = {'UI': 0, 'App': 1, 'Data': 2}
edges = [tuple(p.split(':')) for p in sys.stdin.read().strip().split('=', 1)[1].split(',')]
ok = sum(RANK[u] < RANK[v] for u, v in edges); bad = len(edges) - ok
print(f'valid_edges={ok}\nviolations={bad}\narch_clean={int(bad == 0)}')
