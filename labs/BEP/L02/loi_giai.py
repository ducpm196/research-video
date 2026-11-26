import sys
from collections import defaultdict, deque


def main() -> None:
    kv = dict(line.strip().split("=", 1) for line in sys.stdin.read().splitlines() if "=" in line)
    costs = {}
    for p in kv["nodes"].split(","):
        if ":" in p:
            k, v = p.split(":", 1)
            costs[k] = int(v)
    adj = defaultdict(list)
    ind = {k: 0 for k in costs}
    for e in kv["edges"].split(","):
        if "->" in e:
            u, v = e.split("->", 1)
            adj[u].append(v)
            ind[v] += 1
    q = deque(k for k, d in ind.items() if d == 0)
    dp = dict(costs)
    visited = 0
    while q:
        u = q.popleft()
        visited += 1
        for v in adj[u]:
            dp[v] = max(dp[v], dp[u] + costs[v])
            ind[v] -= 1
            if ind[v] == 0:
                q.append(v)
    has_cycle = int(visited != len(costs))
    crit = -1 if has_cycle else max(dp.values(), default=0)
    print(f"node_count={len(costs)}")
    print(f"has_cycle={has_cycle}")
    print(f"critical_ms={crit}")


if __name__ == "__main__":
    main()
