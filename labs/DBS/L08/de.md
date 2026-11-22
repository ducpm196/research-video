# Lab DBS L08 — SQLite thật: tạo chỉ mục B-Tree (cây B/B+) và lọc khoảng trên 10 000 dòng

Viết tập lệnh SQLite sinh `10 000` dòng `Items(id INT PRIMARY KEY, k INT)`, tạo chỉ mục `CREATE INDEX idx_k ON Items(k)`, xác nhận chỉ mục tồn tại trong `sqlite_master` và lọc khoảng giá trị từ 500 đến 504 (`BETWEEN 500 AND 504`), in đúng 3 dòng:
1. `total_rows=10000`
2. `idx_exists=1`
3. `range_500_504=5`

Chấm tự động:
```bash
bash labs/cham.sh DBS L08 duong_dan/bai_cua_ban.sql
```
