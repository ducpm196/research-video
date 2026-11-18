from math import factorial
from itertools import combinations

def pascal(n):
    hang = [1]
    for _ in range(n):
        moi = [1]
        for i in range(len(hang) - 1):
            moi.append(hang[i] + hang[i + 1])
        moi.append(1)
        hang = moi
    return hang

print('C(12,5):', factorial(12) // (factorial(5) * factorial(7)), pascal(12)[5])
print('hang 8 cua tam giac Pascal:', ' '.join(str(x) for x in pascal(8)))
print('tong hang 6:', sum(pascal(6)))

nguoi = [('nam', i) for i in range(7)] + [('nu', i) for i in range(5)]
co_nu = 0
for nhom in combinations(nguoi, 3):
    if any(p[0] == 'nu' for p in nhom):
        co_nu = co_nu + 1
print('uy ban 3 nguoi, 7 nam 5 nu, it nhat 1 nu:', pascal(12)[3] - pascal(7)[3], co_nu)

d = [[1] * 5 for _ in range(4)]
for r in range(1, 4):
    for c in range(1, 5):
        d[r][c] = d[r - 1][c] + d[r][c - 1]
print('duong di luoi 4 phai 3 len:', pascal(7)[3], d[3][4])
