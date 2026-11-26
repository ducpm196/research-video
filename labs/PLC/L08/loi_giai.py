import sys
s = sys.stdin.read().strip() or "R|R:A;A:B;B:;C:D;D:C;E:"
root, gs = s.split("|", 1)
adj = {k: [x for x in v.split(",") if x] for k, v in (it.split(":", 1) for it in gs.split(";"))}
alive = {root}; q = [root]
while q:
    u = q.pop(0)
    for v in adj[u]:
        if v not in alive: alive.add(v); q.append(v)
reclaimed = sorted(set(adj) - alive)
print(f"alive={sorted(alive)} reclaimed={reclaimed}")
