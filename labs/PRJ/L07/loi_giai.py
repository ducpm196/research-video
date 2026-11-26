import bisect
import hashlib
import sqlite3
import sys


def parse_kv(text: str) -> dict[str, str]:
    kv: dict[str, str] = {}
    for line in text.splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v
    return kv


def h32(s: str) -> int:
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest()[:8], 16)


def owner(n: int, k: int) -> int:
    ring = sorted((h32(f"n{i}#0"), i) for i in range(n))
    return ring[bisect.bisect(ring, (h32(f"k{k}"), 99)) % n][1]


def main() -> None:
    kv = parse_kv(sys.stdin.read())
    commit_ids = [int(x) for x in kv["commit_ids"].split(",") if x]
    rollback_ids = [int(x) for x in kv["rollback_ids"].split(",") if x]
    old_n = int(kv["old_nodes"])
    new_n = int(kv["new_nodes"])
    n_keys = int(kv["keys"])
    events = [int(x) for x in kv["events"].split(",") if x]
    threshold = int(kv["threshold"])

    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE ord(id INT)")
    con.execute("CREATE TABLE outb(id INT)")
    with con:
        for oid in commit_ids:
            con.execute("INSERT INTO ord VALUES(?)", (oid,))
            con.execute("INSERT INTO outb VALUES(?)", (oid,))
    con.execute("BEGIN")
    for rid in rollback_ids:
        con.execute("INSERT INTO ord VALUES(?)", (rid,))
        con.execute("INSERT INTO outb VALUES(?)", (rid,))
    con.rollback()
    c_ord = con.execute("SELECT COUNT(*) FROM ord").fetchone()[0]
    c_out = con.execute("SELECT COUNT(*) FROM outb").fetchone()[0]
    eq = c_ord == c_out and c_ord == len(commit_ids)

    mv = sum(owner(old_n, k) != owner(new_n, k) for k in range(n_keys))

    state = "CLOSED"
    fails = 0
    for ok in events:
        if ok:
            fails = 0
        else:
            fails += 1
            if fails >= threshold:
                state = "OPEN"

    print(f"outbox_atomic_match={int(eq)}")
    print(f"ch_moved_lt_150={int(mv < 0.30 * n_keys)}")
    print(f"cb_after_3fails={state}")


if __name__ == "__main__":
    main()
