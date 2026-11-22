# Lab DBS L11 — SQLite thật: tính nguyên tử ACID với BEGIN, COMMIT và ROLLBACK

Viết tập lệnh SQLite tạo bảng `TK(id TEXT PRIMARY KEY, sd INT CHECK(sd >= 0))` với `('A', 100), ('B', 50)`: thực hiện giao dịch chuyển `40` thành công (`COMMIT`), sau đó mở giao dịch thử trừ `20` ở `A` rồi gọi `ROLLBACK` (huỷ cả giao dịch), in đúng 3 dòng:
1. `after_commit=A:60,B:90`
2. `after_rollback=A:60,B:90`
3. `total_preserved=150`

Chấm tự động:
```bash
bash labs/cham.sh DBS L11 duong_dan/bai_cua_ban.sql
```
