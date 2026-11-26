import sqlite3
import sys
import threading

lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
db = sqlite3.connect(":memory:")
db.executescript(
    "CREATE TABLE acc(id TEXT PRIMARY KEY, bal INT);"
    "CREATE TABLE ent(tx INT, id TEXT, d INT);"
)
locks = {}


def get_lock(acc_id: str) -> threading.Lock:
    if acc_id not in locks:
        locks[acc_id] = threading.Lock()
    return locks[acc_id]


def xfer(tx: int, s: str, d: str, amt: int, fee: int) -> bool:
    if amt <= 0 or fee < 0 or s == d:
        return False
    need_accs = {s, d} | ({"FEE"} if fee > 0 else set())
    ordered = sorted(need_accs)
    acquired = []
    try:
        for k in ordered:
            lk = get_lock(k)
            lk.acquire()
            acquired.append(lk)
        with db:
            rs = db.execute("SELECT bal FROM acc WHERE id=?", (s,)).fetchone()
            rd = db.execute("SELECT bal FROM acc WHERE id=?", (d,)).fetchone()
            rf = db.execute("SELECT bal FROM acc WHERE id='FEE'").fetchone() if fee > 0 else (0,)
            if rs is None or rd is None or rf is None:
                return False
            if rs[0] < amt + fee:
                return False
            db.execute("UPDATE acc SET bal=bal-? WHERE id=?", (amt + fee, s))
            db.execute("UPDATE acc SET bal=bal+? WHERE id=?", (amt, d))
            rows = [(tx, s, -(amt + fee)), (tx, d, amt)]
            if fee > 0:
                db.execute("UPDATE acc SET bal=bal+? WHERE id='FEE'", (fee,))
                rows.append((tx, "FEE", fee))
            db.executemany("INSERT INTO ent VALUES(?,?,?)", rows)
        return True
    finally:
        for lk in reversed(acquired):
            lk.release()


results = []
for ln in lines:
    toks = ln.split()
    if toks[0] == "ACC":
        db.execute("INSERT INTO acc VALUES(?,?)", (toks[1], int(toks[2])))
        get_lock(toks[1])
    elif toks[0] == "TX":
        ok = xfer(int(toks[1]), toks[2], toks[3], int(toks[4]), int(toks[5]))
        results.append("True" if ok else "False")

lsum = db.execute("SELECT COALESCE(SUM(d), 0) FROM ent").fetchone()[0]
bals = db.execute("SELECT id, bal FROM acc ORDER BY id").fetchall()
tot_money = sum(b for _, b in bals)

print("tx_results=" + (",".join(results) if results else "none"))
print(f"ledger_sum={lsum}")
print(f"total_money={tot_money}")
print("balances=" + ",".join(f"{k}:{v}" for k, v in bals))
