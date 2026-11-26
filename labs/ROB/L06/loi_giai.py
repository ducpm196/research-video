import sys, math
s = sys.stdin.read().strip() or "0.75,0.75,0.75,0.75,0.35"
ps = [float(x) for x in s.split(",") if x]
l = sum(math.log(p / (1.0 - p)) for p in ps)
prob = 1.0 / (1.0 + math.exp(-l))
print(f"log_odds={l:.3f} prob={prob:.3f}")
