from fractions import Fraction

x1, x2, x3 = [1, 1, 0], [1, 0, 1], [0, 1, 1]
y = [3, 2, 1]


def dot(u, v):
    return sum(Fraction(a) * b for a, b in zip(u, v))


def bong(x, v):
    c = dot(x, v) / dot(v, v)
    return [c * t for t in v]


def tru(x, cac_bong):
    kq = [Fraction(t) for t in x]
    for b in cac_bong:
        kq = [a - c for a, c in zip(kq, b)]
    return kq


def chuoi(v):
    return "[" + ", ".join(str(t) for t in v) + "]"


v1 = [Fraction(t) for t in x1]
v2 = tru(x2, [bong(x2, v1)])
v3 = tru(x3, [bong(x3, v1), bong(x3, v2)])
print("v1 =", chuoi(v1))
print("v2 =", chuoi(v2))
print("v3 =", chuoi(v3))
print("v1.v2 =", dot(v1, v2))
print("v1.v3 =", dot(v1, v3))
print("v2.v3 =", dot(v2, v3))
print("binh phuong do dai:", chuoi([dot(v, v) for v in (v1, v2, v3)]))
print("toa do cua y:", chuoi([dot(y, v) / dot(v, v) for v in (v1, v2, v3)]))
