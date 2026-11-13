"""Bản thay thế tối thiểu của chương trình dòng lệnh `sqlite3` cho MÁY KIỂM chưa cài sqlite3 (verify_fnd.py đặt vào PATH chỉ khi máy không có
sqlite3 thật). Hỗ trợ đúng phần bài FND dùng: `sqlite3 [-header] [-csv] [TỆP.db] ["SQL" …]`, SQL qua đầu vào chuẩn, các lệnh dấu chấm
.headers on|off, .mode list|csv, .tables, .import [--csv] [--skip N] TỆP BẢNG, .quit. Đầu ra dạng mặc định: cột cách nhau bằng '|'."""
import csv
import sqlite3
import sys

args = sys.argv[1:]
header = False
csvmode = False
db = None
sqls = []
while args:
    a = args.pop(0)
    if a == "-header":
        header = True
    elif a == "-noheader":
        header = False
    elif a == "-csv":
        csvmode = True
    elif a.startswith("-"):
        sys.exit("shim: tuỳ chọn chưa hỗ trợ " + a)
    elif db is None:
        db = a
    else:
        sqls.append(a)
con = sqlite3.connect(db or ":memory:", isolation_level=None)   # tự chốt từng câu như chương trình dòng lệnh thật; BEGIN/COMMIT/ROLLBACK do người dùng điều khiển


def show(cur):
    rows = cur.fetchall()
    if not cur.description:
        return
    if header and rows is not None and cur.description:
        names = [d[0] for d in cur.description]
        print(",".join(names) if csvmode else "|".join(names))
    for r in rows:
        cells = ["" if c is None else str(c) for c in r]
        print(",".join(cells) if csvmode else "|".join(cells))


def run_sql(text):
    buf = ""
    for piece in text.replace(";", ";\x00").split("\x00"):   # tách tại từng dấu ; rồi ghép tới khi đủ một câu lệnh
        buf += piece
        if sqlite3.complete_statement(buf):
            show(con.execute(buf))
            buf = ""
    if buf.strip():
        show(con.execute(buf))


def dot(line):
    global header, csvmode
    parts = line.split()
    c = parts[0]
    if c == ".headers":
        header = parts[1].lower() == "on"
    elif c == ".mode":
        csvmode = parts[1].lower() == "csv"
    elif c == ".print":
        print(line[len(".print"):].strip())
    elif c == ".tables":
        names = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        print("  ".join(names))
    elif c == ".quit":
        con.commit()
        sys.exit(0)
    elif c == ".import":
        skip, rest = 0, parts[1:]
        while rest and rest[0].startswith("--"):
            o = rest.pop(0)
            if o == "--skip":
                skip = int(rest.pop(0))
        path, table = rest
        with open(path, encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        exists = con.execute("SELECT 1 FROM sqlite_master WHERE name=?", (table,)).fetchone()
        if not exists:
            cols = rows[0]
            con.execute(f"CREATE TABLE {table} (" + ",".join(f'"{c_}" TEXT' for c_ in cols) + ")")
            rows = rows[1:]
        else:
            rows = rows[skip:]
        con.execute("BEGIN")
        for r in rows:
            con.execute(f"INSERT INTO {table} VALUES (" + ",".join("?" * len(r)) + ")", r)
        con.execute("COMMIT")
    else:
        sys.exit("shim: lệnh dấu chấm chưa hỗ trợ " + c)


def feed(text):
    pend = ""
    for line in text.splitlines(True):
        if not pend and line.lstrip().startswith("."):
            dot(line.strip())
            continue
        pend += line
        if sqlite3.complete_statement(pend):
            run_sql(pend)
            pend = ""
    if pend.strip():
        run_sql(pend)


if sqls:
    for s in sqls:
        feed(s if s.endswith("\n") else s + "\n")
else:
    feed(sys.stdin.read())
con.commit()
