import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE tk (ten TEXT, so_du INTEGER)")
db.executemany("INSERT INTO tk VALUES (?, ?)",
               [("An", 500), ("Binh", 700), ("Chi", 900), ("Dung", 100)])


def ghep(ten):
    sql = "SELECT ten FROM tk WHERE ten = '" + ten + "'"
    return db.execute(sql).fetchall()


def tham_so(ten):
    sql = "SELECT ten FROM tk WHERE ten = ?"
    return db.execute(sql, (ten,)).fetchall()


CHUOI = ("An", "X' OR '1'='1", "B' OR so_du > 600 --")
for i, ten in enumerate(CHUOI, 1):
    print(f"chuoi {i}: ghep {len(ghep(ten))} dong, tham so {len(tham_so(ten))} dong")
