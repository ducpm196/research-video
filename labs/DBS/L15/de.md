# Lab DBS L15 — SQLite thật: SAVEPOINT và cách cô lập ngăn đọc bẩn (dirty read)

Viết tập lệnh SQLite kiểm chứng bảng `Gia(id INT, v INT)` có `(1, 100)`: mở giao dịch ghi `v=200`, tạo `SAVEPOINT s1`, đổi `v=300` rồi `ROLLBACK TO s1` về lại `200`, cuối cùng `ROLLBACK` về `100`, in đúng 3 dòng:
1. `after_s1_rollback=200`
2. `after_full_rollback=100`
3. `dirty_read_prevented=1`

Chấm tự động:
```bash
bash labs/cham.sh DBS L15 duong_dan/bai_cua_ban.sql
```
