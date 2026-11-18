import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE so (id INT, ver INT)")
db.execute("INSERT INTO so VALUES (2, 3)")
sql = "UPDATE so SET ver = ver + 1 WHERE id = 2 AND ver = ?"
for ten in ("A", "B", "C"):
    print("mua " + ten + ":", db.execute(sql, (3,)).rowcount)
print("phien ban cuoi:", db.execute("SELECT ver FROM so WHERE id = 2").fetchone()[0])

goc, lai_suat = 300000000, 68
lai_du_kien = goc * lai_suat // 1000
lai_som = round(goc * 200 / 365000)
print("lai du kien:", lai_du_kien)
print("lai rut truoc han:", lai_som)
print("mat:", lai_du_kien - lai_som)

CANH = {("CHAO_BAN", "PROCESSING"), ("PROCESSING", "HOLD"),
        ("PROCESSING", "DONE"), ("HOLD", "DONE"), ("HOLD", "REVERT")}
for tu, den in (("HOLD", "DONE"), ("DONE", "HOLD")):
    print(tu, "->", den + ":", "cho phep" if (tu, den) in CANH else "tu choi")
