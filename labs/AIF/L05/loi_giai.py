edges = [(0,1),(0,2),(1,2),(1,3),(2,3),(3,4),(4,5),(2,5)]
ok = 0
for mask in range(3**6):
    c = [(mask // (3**i)) % 3 for i in range(6)]
    if all(c[u] != c[v] for u, v in edges): ok += 1
print(f"total_assign={3**6} valid_solutions={ok}")
