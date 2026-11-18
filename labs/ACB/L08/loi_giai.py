import sqlite3

so_tiet_kiem, ty_le, lai_gui, bien_do = 240000000, 80, 4.8, 2.7
han_muc = so_tiet_kiem * ty_le // 100
lai = round(lai_gui + bien_do, 1)
rut, ngay = 120000000, 45
print("han muc:", han_muc)
print("lai suat:", lai)
print("lai 45 ngay:", round(rut * lai / 100 * ngay / 365))


def mo_han_muc(khoa_ok, cap_ok):
    buoc = []
    if not khoa_ok:
        return ["khoa so loi: dung"]
    buoc.append("khoa so")
    if not cap_ok:
        return buoc + ["cap han muc loi: nha khoa so"]
    return buoc + ["cap han muc"]


print("hai pha:", ",".join(mo_han_muc(True, False)))


def duyet(nhom_no):
    return "duyet tu dong" if nhom_no < 2 else "chuyen tham dinh"


for nhom in (1, 2):
    print("quyet dinh nhom " + str(nhom) + ":", duyet(nhom))

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE giai_ngan (khoa TEXT PRIMARY KEY, tien INT)")
for lan in (1, 2):
    try:
        db.execute("INSERT INTO giai_ngan VALUES ('K7', 120000000)")
        print("giai ngan lan", lan, "chi tien")
    except sqlite3.IntegrityError:
        print("giai ngan lan", lan, "trung khoa, bo qua")
