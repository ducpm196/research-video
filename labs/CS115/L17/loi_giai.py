import math
from fractions import Fraction

k, n = 9, 12
print("MLE dong xu:", Fraction(k, n))
print("MAP (+1 ngua, +1 sap):", Fraction(k + 1, n + 2))
print("MAP (+2 ngua, +2 sap):", Fraction(k + 2, n + 4))


def ln_kha_nang(t):
    return k * math.log(t) + (n - k) * math.log(1 - t)


a, b = round(ln_kha_nang(0.75), 4), round(ln_kha_nang(0.5), 4)
print(f"ln kha nang: theta=0.75 -> {a}, theta=0.5 -> {b}")
print("MLE tot hon:", a > b)
du_lieu = [150, 160, 170, 180]
mu = Fraction(sum(du_lieu), len(du_lieu))
var = sum((x - mu) ** 2 for x in du_lieu) / len(du_lieu)
print("MLE mu, sigma^2:", mu, var)


def chuoi(v):
    return "[" + ", ".join(str(t) for t in v) + "]"


dem = [6, 3, 2, 1]
print("phan loai MLE:", chuoi([Fraction(c, sum(dem)) for c in dem]))
print("phan loai co +1 moi lop:", chuoi([Fraction(c + 1, sum(dem) + 4) for c in dem]))
