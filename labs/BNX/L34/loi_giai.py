import sqlite3

BAC = [(50, "chuyen vien"), (200, "truong phong"), (None, "hoi dong")]
CANH = {("KHOI_TAO", "THAM_DINH"), ("THAM_DINH", "DUYET"),
        ("THAM_DINH", "TU_CHOI")}


def can_ai(du_no, moi):
    tong = du_no + moi
    for tran, vai in BAC:
        if tran is None or tong <= tran:
            return tong, vai


def chuyen(tu, den):
    return "cho phep" if (tu, den) in CANH else "tu choi"


db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE dong_y (khach TEXT, muc_dich TEXT, het_han TEXT, thu_hoi INT)")
db.execute("INSERT INTO dong_y VALUES ('K9', 'tham dinh', '2026-06-30', 0)")


def tra_cuu(khach, muc_dich, ngay):
    sql = "SELECT het_han, thu_hoi FROM dong_y WHERE khach = ? AND muc_dich = ?"
    row = db.execute(sql, (khach, muc_dich)).fetchone()
    if row is None:
        return "tu choi (khong co dong y)"
    if row[1]:
        return "tu choi (da thu hoi)"
    if row[0] < ngay:
        return "tu choi (het han)"
    return "cho phep"


for ten, du_no, moi in (("A", 120, 100), ("B", 0, 40)):
    tong, vai = can_ai(du_no, moi)
    print(f"ho so {ten}: tong {tong} -> {vai}")
print("THAM_DINH -> KHOI_TAO:", chuyen("THAM_DINH", "KHOI_TAO"))
for ngay in ("2026-05-31", "2026-07-01"):
    print("K9 tham dinh", ngay + ":", tra_cuu("K9", "tham dinh", ngay))
