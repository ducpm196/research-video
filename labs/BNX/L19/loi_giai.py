import binascii

KHE = 16384
SO_NUT = 4


def khe(khoa):
    a = khoa.find("{")
    b = khoa.find("}", a + 1)
    if a >= 0 and b > a + 1:          # thẻ băm: chỉ băm phần trong {}
        khoa = khoa[a + 1:b]
    return binascii.crc_hqx(khoa.encode(), 0) % KHE


for khoa in ("loan:disb:B7", "dedup:TX9", "{acc}:5", "{acc}:6"):
    k = khe(khoa)
    print(f"{khoa} -> khe {k}, nut {k // (KHE // SO_NUT) + 1}")


class Kho:
    def __init__(self):
        self.het, self.t = {}, 0

    def set_nx_ex(self, khoa, han):
        if self.het.get(khoa, 0) > self.t:
            return None
        self.het[khoa] = self.t + han
        return "OK"


kho = Kho()
for kho.t in (0, 45, 90, 91):
    print("giay", kho.t, kho.set_nx_ex("dedup:TX9", 90))

print("han danh sach den:", 1000 - 640)
