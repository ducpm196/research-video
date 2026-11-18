from fractions import Fraction

he1 = [[2, 1, -1, 6], [1, 3, 2, 3], [1, 0, -2, 4]]
he2 = [[1, 2, 3, 4], [2, 4, 6, 9], [1, 0, 1, 1]]
he3 = [[1, 2, 3, 4], [2, 4, 6, 8], [1, 0, 1, 1]]


def khu(M):
    M = [[Fraction(x) for x in hang] for hang in M]
    so_cot = len(M[0])
    r = 0
    for c in range(so_cot):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(r + 1, len(M)):
            k = M[i][c] / M[r][c]
            M[i] = [a - k * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return M


def hang(M):
    return sum(1 for hang in khu(M) if any(x != 0 for x in hang))


def the_nguoc(B):
    n = len(B)
    x = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = (B[i][n] - sum(B[i][j] * x[j] for j in range(i + 1, n))) / B[i][i]
    return x


for k, he in enumerate((he1, he2, he3), 1):
    ra = hang([hang_[:3] for hang_ in he])
    rm = hang(he)
    if ra < rm:
        kl = "vo nghiem"
    elif ra < 3:
        kl = "vo so nghiem"
    else:
        x, y, z = the_nguoc(khu(he))
        kl = f"nghiem duy nhat x={x}, y={y}, z={z}"
    print(f"he {k}: hang A={ra}, hang mo rong={rm}, {kl}")
