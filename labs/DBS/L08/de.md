# Lab DBS L08 — SQLite: tạo chỉ mục B-Tree và lọc khoảng trên bảng Items

Cơ sở dữ liệu có sẵn bảng `Items(id INT PRIMARY KEY, k INT)`. Tạo chỉ mục `idx_k` trên `Items(k)` bằng `CREATE INDEX`, đếm tổng dòng, xác nhận chỉ mục tồn tại trong bảng hệ thống `sqlite_master` (`type='index'`, `name='idx_k'`) và đếm số dòng thỏa `k BETWEEN 500 AND 504`.

In đúng 3 dòng: `total_rows=<d>`, `idx_exists=<d>`, `range_500_504=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L08 duong_dan/bai_cua_ban.sql`
