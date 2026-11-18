from fractions import Fraction


def don_hinh(c, A, b, quy_tac, in_ra=False):
    n, m = len(c), len(A)
    ten = [f"x{j + 1}" for j in range(n)] + [f"s{i + 1}" for i in range(m)]
    T = [[Fraction(v) for v in A[i]] + [Fraction(int(i == k)) for k in range(m)] + [Fraction(b[i])] for i in range(m)]
    T.append([Fraction(-v) for v in c] + [Fraction(0)] * (m + 1))
    co_so = [n + i for i in range(m)]
    xoay = 0
    while True:
        am = [j for j in range(n + m) if T[-1][j] < 0]
        if not am:
            break
        cot = min(am) if quy_tac == "chi_so_nho" else min(am, key=lambda j: (T[-1][j], j))
        ung = [(T[i][-1] / T[i][cot], co_so[i], i) for i in range(m) if T[i][cot] > 0]
        _, _, hang = min(ung)
        p = T[hang][cot]
        T[hang] = [v / p for v in T[hang]]
        for i in range(m + 1):
            if i != hang and T[i][cot] != 0:
                f = T[i][cot]
                T[i] = [a - f * r for a, r in zip(T[i], T[hang])]
        xoay += 1
        if in_ra:
            print(f"Xoay {xoay}: cot vao {ten[cot]}, hang ra {ten[co_so[hang]]}, z = {T[-1][-1]}")
        co_so[hang] = cot
    x = [Fraction(0)] * (n + m)
    for i, v in enumerate(co_so):
        x[v] = T[i][-1]
    return T[-1][-1], x[:n], xoay


z, x, k = don_hinh([5, 4], [[6, 4], [1, 2], [-1, 1], [0, 1]], [24, 6, 1, 2], "am_nhat", in_ra=True)
print(f"Toi uu: z = {z}, x1 = {x[0]}, x2 = {x[1]}")
print("So lan xoay:", k)
N = 4
c = [2 ** (N - j) for j in range(1, N + 1)]
A = [[2 ** (i - j + 1) if j < i else (1 if j == i else 0) for j in range(1, N + 1)] for i in range(1, N + 1)]
b = [5 ** i for i in range(1, N + 1)]
print(f"Klee-Minty n = 4: am nhat {don_hinh(c, A, b, 'am_nhat')[2]} lan xoay, chi so nho {don_hinh(c, A, b, 'chi_so_nho')[2]} lan xoay")
