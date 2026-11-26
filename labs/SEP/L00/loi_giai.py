import sys
s = sys.stdin.read().strip() or "0.005 500000 150"
ps, us, ns = s.split()
p, users, n = float(ps), int(us), int(ns)
affected = int(users * p)
prob_zero = (1.0 - p) ** n
print(f"affected={affected} prob_zero_150={prob_zero:.3f}")
