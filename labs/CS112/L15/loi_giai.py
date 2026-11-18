import itertools

INF = float("inf")
C = [[INF, 3, 11, 13], [14, INF, 14, 7], [15, 6, INF, 2], [8, 3, 5, INF]]
n = len(C)
hang = [min(r) for r in C]
R = [[v - m for v in r] for r, m in zip(C, hang)]
cot = [min(R[i][j] for i in range(n)) for j in range(n)]
lb = sum(hang) + sum(cot)
print("min hang:", hang)
print("min cot:", cot)
print("LB goc:", lb)
best = min((sum(C[a][b] for a, b in zip((0,) + p, p + (0,))), p) for p in itertools.permutations(range(1, n)))
print("Toi uu:", best[0], "qua", " ".join(str(x + 1) for x in (0,) + best[1]), "1")
print("LB <= toi uu:", "CO" if lb <= best[0] else "KHONG")


def nut_con(j):
    N = [[v - cot[c] for c, v in enumerate(r)] for r in R]
    chi_phi = N[0][j]
    for k in range(n):
        N[0][k] = INF
        N[k][j] = INF
    N[j][0] = INF
    them = 0
    for i in range(n):
        m = min(N[i])
        if m < INF:
            N[i] = [v - m for v in N[i]]
            them += m
    for c in range(n):
        m = min(N[i][c] for i in range(n))
        if m < INF:
            for i in range(n):
                N[i][c] -= m
            them += m
    return lb + chi_phi + them


print("Nut con 1->2:", nut_con(1))
print("Nut con 1->3:", nut_con(2))
