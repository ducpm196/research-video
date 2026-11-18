import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.executescript("""
CREATE TABLE tk (id INTEGER PRIMARY KEY, so_du INTEGER CHECK (so_du >= 0));
INSERT INTO tk VALUES (1, 500), (2, 400), (3, 300);
""")


def chuyen(a, b, tien):
    try:
        db.execute("BEGIN")
        db.execute("UPDATE tk SET so_du = so_du + ? WHERE id = ?", (tien, b))
        db.execute("UPDATE tk SET so_du = so_du - ? WHERE id = ?", (tien, a))
        db.execute("COMMIT")
        return "OK"
    except sqlite3.IntegrityError:
        db.execute("ROLLBACK")
        return "loi so du khong du"


for a, b, t in [(1, 2, 300), (2, 3, 900), (3, 1, 50), (1, 3, 250)]:
    print(f"chuyen {a}->{b} {t}: {chuyen(a, b, t)}")
print("tong tien:", db.execute("SELECT SUM(so_du) FROM tk").fetchone()[0])
