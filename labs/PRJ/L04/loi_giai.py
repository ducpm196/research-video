import heapq
def dijkstra(edges, src, dst):
    if any(w < 0 for _, _, w in edges):
        raise ValueError('negative edge')
    g = {}
    for u, v, w in edges:
        g.setdefault(u, []).append((v, w))
    dist, pq = {src: 0}, [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == dst:
            return d
        if d > dist.get(u, 10**18):
            continue
        for v, w in g.get(u, []):
            nd = d + w
            if nd < dist.get(v, 10**18):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
edges = [('A', 'D', 15), ('A', 'B', 2), ('B', 'C', 3), ('C', 'D', 4)]
best = dijkstra(edges, 'A', 'D')
neg_rejected = 0
try:
    dijkstra([('A', 'B', -1)], 'A', 'B')
except ValueError:
    neg_rejected = 1
pts = [(1, 3), (2, 5), (3, 7), (4, 9)]
mx = sum(x for x, _ in pts) / len(pts)
my = sum(y for _, y in pts) / len(pts)
den = sum((x - mx) ** 2 for x, _ in pts)
w = sum((x - mx) * (y - my) for x, y in pts) / den
b = my - w * mx
mse = sum((w * x + b - y) ** 2 for x, y in pts) / len(pts)
print(f'min_cost={best} saved_pct={100*(15 - best)/15:.1f}%')
print(f'neg_rejected={neg_rejected}')
print(f'ols_w={w:.1f} ols_b={b:.1f} mse={mse:.2f}')
