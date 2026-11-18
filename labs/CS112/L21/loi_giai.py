import itertools
from fractions import Fraction

rang_buoc = [(1, 1, 9), (3, 1, 18), (1, 0, 7), (0, 1, 6)]
duong = rang_buoc + [(1, 0, 0), (0, 1, 0)]


def hop_le(x, y):
    return x >= 0 and y >= 0 and all(a * x + b * y <= c for a, b, c in rang_buoc)


giai_duoc = 0
dinh = set()
for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(duong, 2):
    det = a1 * b2 - a2 * b1
    if det == 0:
        continue
    giai_duoc += 1
    x = Fraction(c1 * b2 - c2 * b1, det)
    y = Fraction(a1 * c2 - a2 * c1, det)
    if hop_le(x, y):
        dinh.add((x, y))

ds = sorted(dinh, key=lambda p: (3 * p[0] + 2 * p[1], p))
print("Cap duong giai duoc:", giai_duoc)
print("Dinh hop le:", len(ds))
for x, y in ds:
    print(f"({x}, {y}) z = {3 * x + 2 * y}")
x, y = ds[-1]
print(f"Toi uu: z = {3 * x + 2 * y} tai ({x}, {y})")

# y1 + 3*y2 = 3 (he so cua x1), y1 + y2 = 2 (he so cua x2)
y2 = Fraction(3 - 2, 3 - 1)
y1 = 2 - y2
print(f"Chung chi: y1 = {y1}, y2 = {y2}, can tren {y1 * 9 + y2 * 18}")
