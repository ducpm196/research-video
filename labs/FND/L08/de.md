# Lab FND L08 — Bảng và SQL đầu tiên

Viết `so_du.sql` (tệp SQL, chạy được bằng `sqlite3 :memory: < so_du.sql`; cần chương trình `sqlite3` đã cài ở bài đầu, kiểm bằng `sqlite3 --version`), gồm theo thứ tự:

1. `CREATE TABLE giao_dich` với ba cột `INTEGER`: `id` (khoá chính `PRIMARY KEY`), `tk`, `so_tien`.
2. `INSERT INTO giao_dich VALUES` tám hàng `(id, tk, so_tien)`: `(1,1,800000) (2,2,-120000) (3,3,450000) (4,1,300000) (5,2,500000) (6,3,-50000) (7,1,-100000) (8,2,70000)`.
3. Ba câu `SELECT`:
   - số dư từng tài khoản: `tk` và `SUM(so_tien)`, `GROUP BY tk`, `ORDER BY tk`;
   - `SELECT 'tong', SUM(so_tien) FROM giao_dich;`
   - `SELECT 'am', COUNT(*) FROM giao_dich WHERE so_tien < 0;`

Chấm: `bash labs/cham.sh FND L08 so_du.sql` (chạy tệp bằng `sqlite3`). Khác bài giảng: số liệu, số hàng.
