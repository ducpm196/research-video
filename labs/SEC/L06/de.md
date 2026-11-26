# Lab SEC L06 — Phòng thủ XSS bằng html.escape và SQLi bằng ?

Đọc `stdin` `xss=<chuỗi>` (dòng 1) và `sqli=<chuỗi>` (dòng 2). Thực hiện thoát HTML bằng `html.escape(xss)`, tạo bảng SQLite trong bộ nhớ `CREATE TABLE u(n TEXT)` với một dòng khởi tạo `INSERT INTO u VALUES('an')`, rồi chạy truy vấn tham số hóa `SELECT * FROM u WHERE n=?`.

In đúng 3 dòng: `raw_lt_present=<0|1>`, `escaped_len=<d>`, `sqli_rows=<d>`.
Chấm tự động: `bash labs/cham.sh SEC L06 duong_dan/bai_cua_ban.py`
