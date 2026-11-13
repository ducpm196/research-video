# Lab BNK L04 — Sao kê ba tài khoản

Viết tệp `sao_ke.sql` (chạy bằng `python labs/sqlrun.py sao_ke.sql`, hoặc `sqlite3 :memory: < sao_ke.sql` nếu máy có `sqlite3`), gồm theo thứ tự:

1. `CREATE TABLE gd` với ba cột: `id INTEGER PRIMARY KEY`, `tk INTEGER`, `so_tien INTEGER`.
2. `INSERT INTO gd (tk, so_tien) VALUES` bảy dòng `(tk, so_tien)`: `(11, 900000) (12, -200000) (11, -150000) (13, 400000) (12, 600000) (11, 250000) (13, -100000)`.
3. `CREATE INDEX i_gd_tk ON gd (tk);`
4. Ba câu `SELECT`:
   - `id` và `so_tien` của tài khoản 11, `ORDER BY id`;
   - đếm số dòng có `so_tien < 0`;
   - `tk` và `SUM(so_tien)` theo từng tài khoản, `GROUP BY tk`, `ORDER BY tk`.

Chấm: `bash labs/cham.sh BNK L04 sao_ke.sql`.
