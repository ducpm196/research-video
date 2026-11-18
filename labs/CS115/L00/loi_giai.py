from fractions import Fraction

nha = {"P": (3, 2, 2, 12), "Q": (8, 1, 3, 26)}


def sai_so_bp(w, dien_tich, phong, km, gia_that):
    gia_doan = w * dien_tich + 2 * phong - 1 * km
    return (gia_doan - gia_that) ** 2


tot_nhat = None
for w in (2, 3, 4, 5):
    p = sai_so_bp(w, *nha["P"])
    q = sai_so_bp(w, *nha["Q"])
    tong = p + q
    print(f"w={w} P={p} Q={q} tong={tong}")
    if tot_nhat is None or tong < tot_nhat[1]:
        tot_nhat = (w, tong)
print("w tot nhat:", tot_nhat[0])
print("tong nho nhat:", tot_nhat[1])


def w_dung(dien_tich, phong, km, gia_that):
    return Fraction(gia_that - 2 * phong + 1 * km, dien_tich)


print(f"P dung khi w = {w_dung(*nha['P'])}, Q dung khi w = {w_dung(*nha['Q'])}")
