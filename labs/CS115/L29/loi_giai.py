import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
pts = [float(v) for v in kv['pts'].split(',')]
c = [float(v) for v in kv['c'].split(',')]
for _ in range(int(kv['steps'])):
    g = [[], []]
    for x in pts:
        g[0 if abs(x - c[0]) <= abs(x - c[1]) else 1].append(x)
    c = [sum(k) / len(k) if k else c[i] for i, k in enumerate(g)]
inertia = sum(min((x - ci) ** 2 for ci in c) for x in pts)
print(f"centers={c} inertia={inertia:.2f}")
