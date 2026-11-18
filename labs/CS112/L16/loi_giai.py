import itertools
from fractions import Fraction

M = 15
w = [10, 9, 5, 6, 5]
p = [37, 39, 26, 22, 33]
n = len(w)
thu_tu = sorted(range(n), key=lambda i: -Fraction(p[i], w[i]))
print("Thu tu mon:", " ".join(str(i + 1) for i in thu_tu))

x = [Fraction(0)] * n
con_lai = Fraction(M)
tong = Fraction(0)
for i in thu_tu:
    if w[i] <= con_lai:
        x[i] = Fraction(1)
        con_lai -= w[i]
        tong += p[i]
    else:
        x[i] = con_lai / w[i]
        tong += x[i] * p[i]
        break
print("x:", " ".join(str(v) for v in x))
print(f"Tong gia tri: {tong} = {float(tong):.2f}")

con, tham = M, 0
for i in thu_tu:
    if w[i] <= con:
        con -= w[i]
        tham += p[i]
toi_uu = max(sum(p[i] for i in S) for r in range(n + 1) for S in itertools.combinations(range(n), r) if sum(w[i] for i in S) <= M)
print(f"Tham lam 0/1: {tham}, toi uu 0/1: {toi_uu}")
print("Phan so >= 0/1:", "CO" if tong >= toi_uu else "KHONG")
