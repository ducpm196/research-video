import sys
s = sys.stdin.read().strip() or "0,0 6,0 0,6 1,2"
A, B, C, P = [tuple(map(float, pt.split(","))) for pt in s.split()]
edge = lambda Q, U, V: (Q[0]-U[0])*(V[1]-U[1]) - (Q[1]-U[1])*(V[0]-U[0])
tot = edge(C, A, B)
l0, l1, l2 = edge(P, B, C)/tot, edge(P, C, A)/tot, edge(P, A, B)/tot
print(f"bary=({l0:.2f}, {l1:.2f}, {l2:.2f}) inside={int(min(l0, l1, l2) > 0)}")
