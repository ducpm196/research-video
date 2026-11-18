from fractions import Fraction

pts = [(4, 2), (3, 5), (5, 5), (5, 7), (8, 6)]
N = len(pts)
mx = Fraction(sum(p[0] for p in pts), N)
my = Fraction(sum(p[1] for p in pts), N)
print("trung binh:", mx, my)
d = [(p[0] - mx, p[1] - my) for p in pts]
a = sum(v[0] * v[0] for v in d) / N
b = sum(v[0] * v[1] for v in d) / N
print(f"ma tran hiep phuong sai: [[{a}, {b}], [{b}, {a}]]")
l1, l2 = a + b, a - b
print("tri rieng:", l1, "va", l2)
print("vector rieng thu nhat: [1, 1]")
print("ti le phuong sai giu lai (1 thanh phan):", l1 / (l1 + l2))
u = (1, 1)
c = [(v[0] * u[0] + v[1] * u[1]) / (u[0] ** 2 + u[1] ** 2) for v in d]
print("he so tren huong 1:", "[" + ", ".join(str(t) for t in c) + "]")
sai = sum((p[0] - (mx + t * u[0])) ** 2 + (p[1] - (my + t * u[1])) ** 2 for p, t in zip(pts, c))
print("tong binh phuong sai khi khoi phuc:", sai)
