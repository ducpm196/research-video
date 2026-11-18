import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE gd (id INTEGER PRIMARY KEY,"
           " chi_tiet TEXT CHECK (json_valid(chi_tiet)))")
DONG = [(1, '{"kenh":"atm","may":"A7","tien":500000}'),
        (2, '{"kenh":"app","thiet_bi":"d9","tien":200000}'),
        (3, '{"kenh":"atm","may":"B2"'),
        (4, '{"kenh":"app","thiet_bi":"d1","tien":900000}'),
        (5, '{"kenh":"atm","may":"A7","tien":300000}')]
for i, js in DONG:
    try:
        db.execute("INSERT INTO gd VALUES (?, ?)", (i, js))
    except sqlite3.IntegrityError:
        print(f"dong {i}: tu choi (JSON hong)")
tong = db.execute("SELECT SUM(json_extract(chi_tiet, '$.tien')) FROM gd"
                  " WHERE json_extract(chi_tiet, '$.kenh') = 'atm'").fetchone()[0]
print("tong tien kenh atm:", tong)
app = db.execute("SELECT COUNT(*) FROM gd WHERE chi_tiet ->> '$.kenh' = 'app'").fetchone()[0]
print("so giao dich kenh app:", app)
a7 = db.execute("SELECT COUNT(*) FROM gd WHERE chi_tiet ->> '$.may' = 'A7'").fetchone()[0]
print("may A7:", a7, "giao dich")
