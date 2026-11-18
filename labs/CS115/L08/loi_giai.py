from fractions import Fraction

ham = {
    "f1": ([[2, 1], [1, 2]], [3, 0]),
    "f2": ([[2, -3], [-3, 2]], [0, 0]),
    "f3": ([[-2, 0], [0, -4]], [-4, 0]),
    "f4": ([[2, 2], [2, 2]], [2, 2]),
}
for ten, (H, v) in ham.items():
    a, b, c = H[0][0], H[0][1], H[1][1]
    m1, m2 = a, a * c - b * b
    if m2 != 0:
        x = Fraction(c * v[0] - b * v[1], m2)
        y = Fraction(-b * v[0] + a * v[1], m2)
        diem = f"diem dung ({x}, {y})"
    else:
        diem = "khong co diem dung duy nhat"
    if m2 < 0:
        kl = "yen ngua"
    elif m2 == 0:
        kl = "chua ket luan"
    elif m1 > 0:
        kl = "day"
    else:
        kl = "dinh"
    print(f"{ten}: {diem}, dinh thuc con: {m1} va {m2}, ket luan: {kl}")
