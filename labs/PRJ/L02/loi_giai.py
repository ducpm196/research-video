import hashlib
import hmac
import sqlite3
import sys


def verify_token(token: str, secret: bytes, now: int) -> bool:
    parts = token.split(".")
    if len(parts) != 3:
        return False
    sub, exp_s, sig = parts
    if not sub or not exp_s.isdigit():
        return False
    if int(exp_s) < now:
        return False
    expected = hmac.new(secret, f"{sub}.{exp_s}".encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, expected)


def run(text: str) -> str:
    now, secret = 0, b""
    reqs = []
    n_ids, last_id, limit = 0, 0, 10
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        toks = line.split()
        if toks[0].startswith("NOW="):
            now = int(toks[0].split("=", 1)[1])
            secret = toks[1].split("=", 1)[1].encode()
        elif toks[0] == "REQ" and len(toks) == 4:
            reqs.append((toks[1], int(toks[2]), toks[3]))
        elif toks[0] == "IDS":
            n_ids = int(toks[1])
        elif toks[0] == "CURSOR":
            last_id, limit = int(toks[1]), int(toks[2])

    db = sqlite3.connect(":memory:")
    db.executescript("CREATE TABLE idem(k TEXT PRIMARY KEY, a INT); CREATE TABLE tx(id INTEGER PRIMARY KEY);")
    j_ok = j_bad = 0
    for k, amt, tok in reqs:
        if verify_token(tok, secret, now) and amt > 0:
            j_ok += 1
            db.execute("INSERT OR IGNORE INTO idem VALUES(?, ?)", (k, amt))
        else:
            j_bad += 1
    cnt, tot = db.execute("SELECT COUNT(*), COALESCE(SUM(a), 0) FROM idem").fetchone()
    if n_ids > 0:
        with db:
            db.executemany("INSERT INTO tx(id) VALUES(?)", [(i,) for i in range(1, n_ids + 1)])
    ids = [str(r[0]) for r in db.execute("SELECT id FROM tx WHERE id > ? ORDER BY id LIMIT ?", (last_id, limit))]
    page = ",".join(ids) if ids else "none"
    return f"jwt_valid={j_ok} jwt_invalid={j_bad}\nexecuted={cnt} total_amount={tot}\ncursor_page={page}"


if __name__ == "__main__":
    print(run(sys.stdin.read()))
