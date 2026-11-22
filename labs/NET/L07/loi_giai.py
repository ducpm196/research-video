import heapq
adj = {k: [] for k in 'SABCD'}
for u, v, w in [('S','A',4),('S','B',1),('A','B',2),('A','C',1),('B','C',5),('B','D',8),('C','D',3)]:
    adj[u].append((v, w)); adj[v].append((u, w))
d = {'S': 0}; nh = {}; pq = [(0, 'S')]
while pq:
    c, u = heapq.heappop(pq)
    if c > d.get(u, 99): continue
    for v, w in adj[u]:
        if c + w < d.get(v, 99):
            d[v] = c + w; nh[v] = v if u == 'S' else nh[u]
            heapq.heappush(pq, (d[v], v))
hops = ''.join(sorted({nh[k] for k in 'ABCD'}))
print('dist=' + ','.join(f'{k}:{d[k]}' for k in 'ABCD'))
print(f'next_hop_all={hops}')
print(f'sa_direct_vs_sb_ba=4_vs_{d["A"]}')
