def rel(u, v):
    le = all(a <= b for a, b in zip(u, v)); ge = all(a >= b for a, b in zip(u, v))
    if u == v: return 'equal'
    if le: return 'before'
    return 'after' if ge else 'concurrent'
r1 = rel((1,0,0), (2,0,1)); r2 = rel((2,0,1), (1,2,0))
print(f'v100_vs_v201={r1}')
print(f'v201_vs_v120={r2}')
print(f'partial_order_ok={int(r1 == "before" and r2 == "concurrent")}')
