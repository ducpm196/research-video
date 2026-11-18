from fractions import Fraction


def dinh_thuc(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def nghich_dao(M):
    dt = Fraction(dinh_thuc(M))
    return [[M[1][1] / dt, -M[0][1] / dt], [-M[1][0] / dt, M[0][0] / dt]]


def nhan_vec(A, v):
    return [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]


def chuoi(v):
    if isinstance(v[0], list):
        return "[" + ", ".join(chuoi(r) for r in v) + "]"
    return "[" + ", ".join(str(t) for t in v) + "]"


M, b = [[5, 2], [7, 3]], [9, 13]
Mn = nghich_dao(M)
w = nhan_vec(Mn, b)
print("dinh thuc M:", dinh_thuc(M))
print("M nghich dao:", chuoi(Mn))
print("w:", chuoi(w))
print("M.w:", chuoi(nhan_vec(M, w)))
for t in (Fraction(1, 100), Fraction(1, 10000)):
    Mt = [[1, 1], [1, 1 + t]]
    Mi = nghich_dao(Mt)
    lon = max(abs(x) for r in Mi for x in r)
    print(f"t={t}: dinh thuc {dinh_thuc(Mt)}, nghich dao lon nhat {lon}, w doi {chuoi(nhan_vec(Mi, [0, Fraction(1, 1000)]))}")
X = [[1, 1], [1, 2], [1, 3]]
y = [2, 2, 4]
XtX = [[sum(r[i] * r[j] for r in X) for j in range(2)] for i in range(2)]
Xty = [sum(r[i] * t for r, t in zip(X, y)) for i in range(2)]
print("hoi quy: w =", chuoi(nhan_vec(nghich_dao(XtX), Xty)))
X2 = [[1, 1], [3, 3], [5, 5]]
A2 = [[sum(r[i] * r[j] for r in X2) for j in range(2)] for i in range(2)]
print("hai cot giong nhau: dinh thuc X^T X =", dinh_thuc(A2))
