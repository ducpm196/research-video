import heapq, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
nodes = list(kv['nodes']); src = kv['src']; adj = {k: [] for k in nodes}
direct_a = None
for e in kv['edges'].split(','):
    uv, ws = e.split(':'); u, v = uv.split('-'); w = int(ws)
    adj[u].append((v, w)); adj[v].append((u, w))
    if {u, v} == {src, 'A'}: direct_a = w
d = {src: 0}; nh = {}; pq = [(0, src)]
while pq:
    c, u = heapq.heappop(pq)
    if c > d.get(u, 10**9): continue
    for v, w in adj[u]:
        if c + w < d.get(v, 10**9):
            d[v] = c + w; nh[v] = v if u == src else nh[u]
            heapq.heappush(pq, (d[v], v))
others = [k for k in nodes if k != src]
hops = ''.join(sorted({nh[k] for k in others}))
print('dist=' + ','.join(f'{k}:{d[k]}' for k in others))
print(f'next_hop_all={hops}')
print(f'sa_direct_vs_sb_ba={direct_a}_vs_{d["A"]}')
