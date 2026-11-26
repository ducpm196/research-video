import sqlite3
import sys

lines = sys.stdin.read().splitlines()
ok = []
bad = 0
in_tot = 0
out_tot = 0
acc_py = {}

for raw in lines:
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) == 3:
        acc, tp, amt = parts
        if acc and tp in ("IN", "OUT") and amt.isdigit() and int(amt) > 0:
            v = int(amt)
            ok.append((acc, tp, v))
            if tp == "IN":
                in_tot += v
                acc_py[acc] = acc_py.get(acc, 0) + v
            else:
                out_tot += v
                acc_py[acc] = acc_py.get(acc, 0) - v
            continue
    bad += 1

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE ledger(acc TEXT, tp TEXT, v INT)")
with db:
    db.executemany("INSERT INTO ledger VALUES(?,?,?)", ok)

sql_net = db.execute(
    "SELECT COALESCE(SUM(CASE WHEN tp='IN' THEN v ELSE -v END), 0) FROM ledger"
).fetchone()[0]
sql_acc = dict(
    db.execute(
        "SELECT acc, SUM(CASE WHEN tp='IN' THEN v ELSE -v END) FROM ledger GROUP BY acc ORDER BY acc"
    ).fetchall()
)
assert sql_acc == {k: acc_py[k] for k in sorted(acc_py)}

tot = len(lines)
pct = (100.0 * len(ok) / tot) if tot else 0.0
py_net = in_tot - out_tot
acc_str = ",".join(f"{k}:{sql_acc[k]}" for k in sorted(sql_acc)) if sql_acc else "none"

print(f"valid={len(ok)} bad={bad} valid_pct={pct:.1f}%")
print(f"py_net={py_net} sql_net={sql_net}")
print(f"in_total={in_tot} out_total={out_tot}")
print(f"acc_nets={acc_str}")
