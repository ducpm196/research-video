def bando(truong):
    bits = 0
    for n in truong:
        bits = bits | (1 << (64 - n))
    return format(bits, "016X")


def giai_ma(hex16):
    v = int(hex16, 16)
    return [n for n in range(1, 65) if v >> (64 - n) & 1]


print("bitmap A:", bando([3, 4, 11, 37, 41]))
cac_truong = [3, 4, 11, 37, 128]
chinh = [1] + [n for n in cac_truong if n <= 64]
phu = [n - 64 for n in cac_truong if n > 64]
print("bitmap B:", bando(chinh), bando(phu))
print("giai ma:", giai_ma("5030000000000000"))

ket = {}


def dat(khoa, bay_gio, ttl):
    if khoa in ket and ket[khoa] > bay_gio:
        return False
    ket[khoa] = bay_gio + ttl
    return True


ttl = 2 * 40
for t, nhan in ((0, "khoa moi"), (30, "khoa trung"), (95, "het han")):
    print("t=" + str(t), nhan + ":", dat("654321:000000000007", t, ttl))
print("dang cho:", 2400 * 150 // 1000)
