import sys
n = int(sys.stdin.read().split('=')[1])
u = n * (n - 1); f = n - 1
print(f'unbounded_edges={u}')
print(f'facade_edges={f}')
print(f'edge_reduction_pct={100 * (u - f) / u:.1f}%')
