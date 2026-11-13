"""Chạy một tệp .sql bằng mô-đun sqlite3 của Python và in kết quả đúng dạng mặc định của `sqlite3` (cột cách nhau bằng '|').
Dùng khi máy chưa có chương trình dòng lệnh sqlite3. Chỉ hỗ trợ câu lệnh SQL thường (không có lệnh dấu chấm như .headers)."""
import sqlite3
import sys

con = sqlite3.connect(":memory:")
buf = ""
for line in open(sys.argv[1], encoding="utf-8"):
    if not buf and line.lstrip().startswith("."):
        sys.exit("lệnh dấu chấm không hỗ trợ ở bản chạy bằng Python: " + line.strip())
    buf += line
    if sqlite3.complete_statement(buf):
        cur = con.execute(buf)
        for row in cur.fetchall():
            print("|".join("" if c is None else str(c) for c in row))
        buf = ""
if buf.strip():
    for row in con.execute(buf).fetchall():
        print("|".join("" if c is None else str(c) for c in row))
