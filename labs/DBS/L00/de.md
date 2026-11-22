# Lab DBS L00 — SQLite thật: khoá chính (PK), khoá ngoại (FK) và toàn vẹn tham chiếu

Viết tập lệnh SQLite (`*.sql`) bật kiểm khoá ngoại `PRAGMA foreign_keys = ON;`, tạo `Lop(ma TEXT PRIMARY KEY)` có `'K1'`, `SV(id INT PRIMARY KEY, ten TEXT, lop TEXT REFERENCES Lop(ma))`, thử `INSERT OR IGNORE` (chèn, bỏ qua nếu trùng khoá chính `PK`) `(1,'An','K1')`, `(1,'Trung', 'K1')`, chặn dòng sai khoá ngoại `FK` `(2,'Em','K9')` rồi `SELECT` ra đúng 3 dòng:
1. `sv_count=1`
2. `k9_blocked=1`
3. `null_fk_allowed=1`

Chấm tự động:
```bash
bash labs/cham.sh DBS L00 duong_dan/bai_cua_ban.sql
```
