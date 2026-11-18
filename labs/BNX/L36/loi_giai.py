import math

KHACH, GD_KHACH, DINH, NUT = 50_000, 4, 8, 500
for he_so in (1, 1000):
    gd = KHACH * he_so * GD_KHACH
    tb = gd / 86_400
    dinh = tb * DINH
    nut = math.ceil(dinh / NUT)
    if nut == 1:
        chon = "mot nut"
    elif nut <= 10:
        chon = "nhom nut"
    else:
        chon = "chia theo khoa"
    print(f"x{he_so}: tb {tb:.1f}/s, dinh {dinh:.0f}/s, {nut} nut -> {chon}")

so_du = {"A": 500, "B": 0}
da_xu_ly = {}


def chuyen(khoa, tu, den, tien):
    if khoa in da_xu_ly:
        return "trung khoa, bo qua"
    da_xu_ly[khoa] = (tu, den, tien)
    so_du[tu] -= tien
    so_du[den] += tien
    return "da chuyen"


for lan in (1, 2):
    print(f"lan {lan}:", chuyen("K9", "A", "B", 200))
print(f"so du: A={so_du['A']} B={so_du['B']}")
