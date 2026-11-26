import sys, math
s = sys.stdin.read().strip() or "0.0001 0.85 0.95"
eps, g1, g2 = map(float, s.split())
k1 = math.ceil(math.log(eps) / math.log(g1))
k2 = math.ceil(math.log(eps) / math.log(g2))
print(f"iters_g085={k1} iters_g095={k2}")
