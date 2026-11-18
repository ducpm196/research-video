from fractions import Fraction

x, y = [1, 2, 4, 5], [2, 1, 5, 4]
n = len(x)
mx, my = Fraction(sum(x), n), Fraction(sum(y), n)
dx, dy = [a - mx for a in x], [b - my for b in y]
vx = sum(a * a for a in dx) / n
vy = sum(b * b for b in dy) / n
cov = sum(a * b for a, b in zip(dx, dy)) / n
print("trung binh:", mx, my)
print("phuong sai:", vx, vy)
print("hiep phuong sai:", cov)
print("tuong quan:", cov / vx)
S = [[vx, cov], [cov, vy]]
dt = vx * vy - cov * cov
print(f"ma tran: [[{S[0][0]}, {S[0][1]}], [{S[1][0]}, {S[1][1]}]]")
print("dinh thuc:", dt)
Sn = [[vy / dt, -cov / dt], [-cov / dt, vx / dt]]


def mahal2(d):
    t = [Sn[0][0] * d[0] + Sn[0][1] * d[1], Sn[1][0] * d[0] + Sn[1][1] * d[1]]
    return d[0] * t[0] + d[1] * t[1]


print("khoang cach theo do trai^2 cua (5, 5):", mahal2((2, 2)))
print("khoang cach theo do trai^2 cua (5, 1):", mahal2((2, -2)))
print("khoang cach thang^2 cua ca hai:", 2**2 + 2**2)
