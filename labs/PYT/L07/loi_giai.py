class SoTienAm(Exception):
    pass

def doc_so_tien(chuoi):
    so = int(chuoi.replace(".", ""))
    if so < 0:
        raise SoTienAm(chuoi)
    return so

giao_dich = ["2.500.000", "75.000", "n/a", "", "-30.000", "1.000.000"]
tong = 0
da_xu_ly = 0
for chuoi in giao_dich:
    try:
        tong = tong + doc_so_tien(chuoi)
    except ValueError:
        print("Bo qua (dinh dang):", repr(chuoi))
    except SoTienAm:
        print("Bo qua (am):", chuoi)
    finally:
        da_xu_ly = da_xu_ly + 1
print("Tong:", tong)
print("Da xu ly:", da_xu_ly)
