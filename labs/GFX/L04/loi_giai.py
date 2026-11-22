edge = lambda P, U, V: (P[0]-U[0])*(V[1]-U[1]) - (P[1]-U[1])*(V[0]-U[0])
A, B, C, P = (0, 0), (6, 0), (0, 6), (1, 2)
tot = edge(C, A, B)
l0 = edge(P, B, C) / tot
l1 = edge(P, C, A) / tot
l2 = edge(P, A, B) / tot
print(f"bary=({l0:.2f}, {l1:.2f}, {l2:.2f}) inside={int(min(l0, l1, l2) > 0)}")
