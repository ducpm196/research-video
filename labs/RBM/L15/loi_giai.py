import sys, heapq
s = sys.stdin.read().strip() or "4 5 1 0 1 4|0,2;1,2;2,2"
hdr, w_str = s.split("|", 1)
R, C, sr, sc, gr, gc = map(int, hdr.split())
walls = {tuple(map(int, x.split(","))) for x in w_str.split(";") if x}
start, goal = (sr, sc), (gr, gc)
h = lambda p: abs(p[0]-goal[0]) + abs(p[1]-goal[1])
pq = [(h(start), 0, start)]; dist = {start: 0}
while pq:
    _, g, u = heapq.heappop(pq)
    if u == goal: print(f"astar_steps={g} h_start={h(start)}"); break
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
        v = (u[0]+dr, u[1]+dc)
        if 0 <= v[0] < R and 0 <= v[1] < C and v not in walls and g+1 < dist.get(v, 9999):
            dist[v] = g + 1; heapq.heappush(pq, (g + 1 + h(v), g + 1, v))
