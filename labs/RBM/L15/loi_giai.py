import heapq
walls = {(0, 2), (1, 2), (2, 2)}; start, goal = (1, 0), (1, 4)
h = lambda p: abs(p[0]-goal[0]) + abs(p[1]-goal[1])
pq = [(h(start), 0, start)]; dist = {start: 0}
while pq:
    _, g, u = heapq.heappop(pq)
    if u == goal: print(f"astar_steps={g} h_start={h(start)}"); break
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
        v = (u[0]+dr, u[1]+dc)
        if 0 <= v[0] < 4 and 0 <= v[1] < 5 and v not in walls and g+1 < dist.get(v, 99):
            dist[v] = g + 1; heapq.heappush(pq, (g + 1 + h(v), g + 1, v))
