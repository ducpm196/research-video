# Lab DBS L07 — SQLite thật: kiểm tra quét tuần tự SCAN trên bảng không chỉ mục

Viết tập lệnh SQLite sinh `1 000` dòng vào bảng `Logs(id INT, code INT)` bằng CTE đệ quy (`WITH RECURSIVE`, không tạo chỉ mục), kiểm tra bảng hệ thống `sqlite_master` xác nhận không có chỉ mục (`EXPLAIN QUERY PLAN` — kế hoạch thực thi — sẽ `SCAN Logs` quét toàn bảng), in đúng 3 dòng:
1. `row_count=1000`
2. `plan_uses_scan=1`
3. `hits_42=10`

Chấm tự động:
```bash
bash labs/cham.sh DBS L07 duong_dan/bai_cua_ban.sql
```
