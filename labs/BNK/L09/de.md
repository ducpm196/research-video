# Lab BNK L09 — Hai giao dịch, một giao dịch lệch

Viết tệp `so_cai.sql` (chạy bằng `python labs/sqlrun.py so_cai.sql`, hoặc `sqlite3 :memory: < so_cai.sql`):

1. `CREATE TABLE but_toan (gd INTEGER, tk TEXT, tien INTEGER);`
2. Giao dịch 1 (có phí): `('C', -1206600)`, `('D', 1200000)`, `('phi', 6600)`.
3. Giao dịch 2: `('C', -50000)`, `('D', 40000)` — **cố ý lệch**.
4. Câu `SELECT` tìm mã giao dịch có tổng khác 0 (`GROUP BY gd HAVING SUM(tien) <> 0`).
5. Câu `SELECT` số dư mỗi tài khoản: `tk`, `SUM(tien)`, `GROUP BY tk`, `ORDER BY tk`.

Chấm: `bash labs/cham.sh BNK L09 so_cai.sql`.
