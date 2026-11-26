# Lab SWF L12 — Đối chiếu ghép chuỗi vs truy vấn tham số hoá thật trên SQLite

Đọc `stdin` một dòng chứa `payload=<chuỗi>`. Tạo bảng `CREATE TABLE u(n TEXT, r TEXT)` trong bộ nhớ bằng `sqlite3` và chèn 2 dòng `('an', 'user'), ('root', 'admin')`. Chạy cả câu truy vấn ghép chuỗi `f"SELECT * FROM u WHERE n='{payload}'"` lẫn câu truy vấn tham số hoá `SELECT * FROM u WHERE n=?` rồi đếm số dòng trả về.

In đúng 3 dòng: `unsafe_rows_leaked=<d>`, `param_rows_returned=<d>`, `sqli_blocked=<0|1>` (với `sqli_blocked = 1` nếu `len(safe) == 0`).
Chấm tự động: `bash labs/cham.sh SWF L12 duong_dan/bai_cua_ban.py`
