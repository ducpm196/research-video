import sys
n = int(dict(t.split('=') for t in sys.stdin.read().split())['n'])
naive = {i: (i + 1) % n for i in range(n)}
cur, seen = 0, []
while cur not in seen: seen.append(cur); cur = naive[cur]
edges_ord = [(min(i, (i + 1) % n), max(i, (i + 1) % n)) for i in range(n)]
has_cycle = any(a >= b for a, b in edges_ord)
print(f'naive_cycle_len={len(seen)}')
print(f'ordered_cycle={int(has_cycle)}')
print(f'coffman_broken={"circular_wait" if not has_cycle else "none"}')
