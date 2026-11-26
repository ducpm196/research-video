import hashlib
import hmac
import sqlite3
import sys


def main() -> None:
    kv: dict[str, str] = {}
    for line in sys.stdin.read().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k.strip()] = v
    key = kv["key"].encode("utf-8")
    msg = kv["msg"]
    probe = kv["probe"]

    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE log(id INT PRIMARY KEY, m TEXT, mac TEXT)")
    con.execute("CREATE INDEX idx_m ON log(m)")
    mac = hmac.new(key, msg.encode("utf-8"), hashlib.sha256).hexdigest()
    con.execute("INSERT INTO log VALUES(?, ?, ?)", (1, msg, mac))

    bad = con.execute("SELECT * FROM log WHERE m=?", (probe,)).fetchall()
    row_m, row_sig = con.execute("SELECT m, mac FROM log WHERE id=1").fetchone()
    expected = hmac.new(key, row_m.encode("utf-8"), hashlib.sha256).hexdigest()
    ok = hmac.compare_digest(row_sig, expected)

    print(f"mac_len={len(mac)}")
    print(f"sqli_blocked={int(len(bad) == 0)}")
    print(f"hmac_verified={int(ok)}")


if __name__ == "__main__":
    main()
