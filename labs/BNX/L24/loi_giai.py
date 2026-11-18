import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE khach (id INTEGER PRIMARY KEY, ten TEXT);
CREATE TABLE the (id INTEGER PRIMARY KEY, khach_id INTEGER, han_muc INTEGER);
""")
for i in range(1, 13):
    db.execute("INSERT INTO khach VALUES (?, ?)", (i, f"K{i}"))
    for j in range(1, 4):
        db.execute("INSERT INTO the VALUES (?, ?, ?)", (i * 10 + j, i, 2000000 * j))
db.commit()

dem = 0
def dem_sql(cau):
    global dem
    dem += 1

db.set_trace_callback(dem_sql)

# Cach 1: 1 cau lay khach, roi moi khach 1 cau lay the
tong = 0
for (kid,) in db.execute("SELECT id FROM khach").fetchall():
    tong += len(db.execute("SELECT id FROM the WHERE khach_id = ?", (kid,)).fetchall())
print(f"Cach 1: {dem} cau, tong so the {tong}")

# Cach 2: mot cau noi hai bang
dem = 0
dong = db.execute("SELECT k.id, t.id FROM khach k JOIN the t ON t.khach_id = k.id").fetchall()
print(f"Cach 2: {dem} cau, tong so the {len(dong)}")
