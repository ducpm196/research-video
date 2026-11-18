from fractions import Fraction


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def chieu(y, u):
    tu, mau = dot(y, u), dot(u, u)
    c = Fraction(tu, mau)
    hc = [c * x for x in u]
    z = [a - b for a, b in zip(y, hc)]
    return tu, mau, c, hc, z


def ghep(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


y, u = [7, 4, 1], [2, 0, 1]
tu, mau, c, hc, z = chieu(y, u)
print("tu so:", tu)
print("mau so:", mau)
print("c =", c)
print("hinh chieu:", ghep(hc))
print("phan con lai z:", ghep(z))
print("z.u =", dot(z, u))
print(f"Pytago: {dot(y, y)} = {dot(hc, hc)} + {dot(z, z)}")

tu, mau, c, hc, z = chieu([2, 3], [4, 1])
print("c =", c)
print("hinh chieu:", ghep(hc))
