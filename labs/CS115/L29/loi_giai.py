pts = [1.0, 2.0, 8.0, 10.0]
c = [1.0, 8.0]
for _ in range(2):
    g = [[], []]
    for x in pts:
        g[0 if abs(x - c[0]) <= abs(x - c[1]) else 1].append(x)
    c = [sum(k) / len(k) for k in g]
inertia = sum(min((x - ci) ** 2 for ci in c) for x in pts)
print(f"centers={c} inertia={inertia:.2f}")
