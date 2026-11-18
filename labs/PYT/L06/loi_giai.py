class TaiKhoan:
    def __init__(self, ma, so_du=0, thau_chi=0):
        self.ma = ma
        self.so_du = so_du
        self.thau_chi = thau_chi

    def nap(self, tien):
        if tien <= 0:
            return False
        self.so_du = self.so_du + tien
        return True

    def rut(self, tien):
        if tien <= 0 or self.so_du - tien < -self.thau_chi:
            return False
        self.so_du = self.so_du - tien
        return True

    def __repr__(self):
        return f"TaiKhoan({self.ma}, {self.so_du})"

a = TaiKhoan("B07", 2000000, thau_chi=500000)
print(a.rut(2400000), a)
print(a.rut(200000), a)
print(a.nap(600000), a)
print(a.nap(-5), a)
b = TaiKhoan("B08")
print(b)

import sys
import tracemalloc

so = [i for i in range(1000)]
chuoi = ["x" * 100 + str(i) for i in range(1000)]
print("getsizeof hai danh sach:", "bang nhau" if sys.getsizeof(so) == sys.getsizeof(chuoi) else "khac nhau")


def dung(tao):
    tracemalloc.start()
    xs = tao()
    dang_dung = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()
    return dang_dung


m_so = dung(lambda: [i for i in range(1000)])
m_chuoi = dung(lambda: ["x" * 100 + str(i) for i in range(1000)])
print("tracemalloc hai danh sach:", "chuoi lon hon" if m_chuoi > m_so else "so lon hon")
