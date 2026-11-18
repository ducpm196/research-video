def chep(n, tang):
    # mảng động bắt đầu sức chứa 1; thêm n phần tử; khi đầy thì sức chứa mới = tang(sức chứa cũ), chép hết phần tử đang có
    suc_chua, so_chep = 1, 0
    for dang_co in range(n):
        if dang_co == suc_chua:
            so_chep += dang_co
            suc_chua = tang(suc_chua)
    return so_chep


class Nut:
    def __init__(self, gia_tri, tiep=None):
        self.gia_tri = gia_tri
        self.tiep = tiep


def chen_dau(dau, gia_tri):
    return Nut(gia_tri, dau)


def duyet(dau):
    ket_qua = []
    while dau is not None:
        ket_qua.append(dau.gia_tri)
        dau = dau.tiep
    return ket_qua


for n in (1000, 5000):
    print(f"n = {n} gap doi: {chep(n, lambda s: s * 2)} lan chep")
    print(f"n = {n} them 10 o: {chep(n, lambda s: s + 10)} lan chep")
dau = Nut(1, Nut(2))
for x in (5, 6, 7):
    dau = chen_dau(dau, x)
print("sau khi chen 5, 6, 7 vao dau:", " -> ".join(str(x) for x in duyet(dau)))
