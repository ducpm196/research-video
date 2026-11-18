class Nut:
    def __init__(self, khoa, trai=None, phai=None):
        self.khoa = khoa
        self.trai = trai
        self.phai = phai


def them(goc, khoa):
    if goc is None:
        return Nut(khoa)
    if khoa < goc.khoa:
        goc.trai = them(goc.trai, khoa)
    else:
        goc.phai = them(goc.phai, khoa)
    return goc


def duyet_giua(nut):
    return [] if nut is None else duyet_giua(nut.trai) + [nut.khoa] + duyet_giua(nut.phai)


def duyet_truoc(nut):
    return [] if nut is None else [nut.khoa] + duyet_truoc(nut.trai) + duyet_truoc(nut.phai)


def chieu_cao(nut):
    return -1 if nut is None else 1 + max(chieu_cao(nut.trai), chieu_cao(nut.phai))


def la_cay_tim_kiem(nut):
    day = duyet_giua(nut)
    return all(day[i] < day[i + 1] for i in range(len(day) - 1))


goc = None
for k in (50, 30, 70, 20, 40, 60, 80, 10, 45):
    goc = them(goc, k)
print("giua:", " ".join(map(str, duyet_giua(goc))))
print("truoc:", " ".join(map(str, duyet_truoc(goc))))
print("chieu cao:", chieu_cao(goc))
print("he so goc:", chieu_cao(goc.trai) - chieu_cao(goc.phai))
hang = None
for k in range(1, 8):
    hang = them(hang, k)
print("chen 1..7 theo thu tu: chieu cao", chieu_cao(hang))
hong = Nut(8, Nut(3, Nut(1), Nut(9)), Nut(10))
print("cay hong:", "dung" if la_cay_tim_kiem(hong) else "sai")
print("cay tot:", "dung" if la_cay_tim_kiem(goc) else "sai")
