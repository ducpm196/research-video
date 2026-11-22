import math
dist = lambda u, v: math.hypot(u[0] - v[0], u[1] - v[1])
A, B, Q = (20, 2000), (50, 2000), (20, 3000)
scale = lambda p: (p[0] / 40.0, p[1] / 1000.0)
print(f"raw_dQA={dist(Q, A):.1f} raw_dQB={dist(Q, B):.2f}")
print(f"norm_dQA={dist(scale(Q), scale(A)):.3f} norm_dQB={dist(scale(Q), scale(B)):.3f}")
