import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE hang_doi (id INTEGER PRIMARY KEY AUTOINCREMENT,"
           " ma_gd INTEGER, so_tien INTEGER)")


def gui(ma, tien, chot):
    db.execute("BEGIN")
    db.execute("INSERT INTO hang_doi (ma_gd, so_tien) VALUES (?, ?)", (ma, tien))
    db.execute("COMMIT" if chot else "ROLLBACK")


def nhan():
    db.execute("BEGIN")
    dong = db.execute("SELECT id, ma_gd, so_tien FROM hang_doi"
                      " ORDER BY id LIMIT 1").fetchone()
    if dong:
        db.execute("DELETE FROM hang_doi WHERE id = ?", (dong[0],))
    db.execute("COMMIT")
    return dong


def dem():
    return db.execute("SELECT COUNT(*) FROM hang_doi").fetchone()[0]


gui(201, 750000, True)
gui(202, 300000, False)
gui(203, 120000, True)
gui(204, 900000, True)
print("sau gui:", dem(), "thong diep")
for _ in range(2):
    _, ma, tien = nhan()
    print("nhan:", ma, tien)
print("con lai:", dem())
LENH = [(3, 8), (4, 9), (7, 11), (10, 14), (6, 13)]
xuyen = sum(1 for a, b in LENH if a % 4 != b % 4)
print(f"xuyen manh: {xuyen}/{len(LENH)}")
