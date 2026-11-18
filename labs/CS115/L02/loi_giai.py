from fractions import Fraction


def nhan(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def dinh_thuc(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def nghich_dao(M):
    dt = dinh_thuc(M)
    if dt == 0:
        return None
    a, b, c, d = M[0][0], M[0][1], M[1][0], M[1][1]
    return [[Fraction(d, dt), Fraction(-b, dt)], [Fraction(-c, dt), Fraction(a, dt)]]


def chuoi(x):
    if isinstance(x, list):
        return "[" + ", ".join(chuoi(t) for t in x) + "]"
    return str(x)


A, B = [[2, 0], [1, 3]], [[1, 4], [2, 5]]
print("AB =", chuoi(nhan(A, B)))
print("BA =", chuoi(nhan(B, A)))
print("AB khac BA:", nhan(A, B) != nhan(B, A))

M, b = [[3, 1], [5, 2]], [13, 22]
print("dinh thuc M:", dinh_thuc(M))
Mn = nghich_dao(M)
print("M nghich dao:", chuoi(Mn))
w = [sum(Mn[i][k] * b[k] for k in range(2)) for i in range(2)]
print("w =", chuoi(w))
print("M.w =", chuoi([sum(M[i][k] * w[k] for k in range(2)) for i in range(2)]))
