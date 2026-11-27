# Lab DBS L00 — SQLite: khoá chính (PK), khoá ngoại (FK) và toàn vẹn tham chiếu

Cơ sở dữ liệu khởi tạo sẵn hai bảng `Lop(ma)`, `SV(id, ten, lop REFERENCES Lop)` cùng bảng tạm `NhapSV(id, ten, lop)`. Viết tập lệnh SQLite bật `PRAGMA foreign_keys = ON;`, chèn bỏ qua trùng PK và lọc các dòng có mã lớp tồn tại trong `Lop` từ `NhapSV` sang `SV` (dùng `INSERT OR IGNORE` kèm `WHERE EXISTS`), thêm `(6,'Ha',NULL)`, rồi xuất 3 dòng `'sv_count=' || ...`, `k9_blocked=<0|1>`, `null_fk_allowed=<0|1>` (kiểm bằng `IS NULL`).

Chấm tự động: `bash labs/cham.sh DBS L00 duong_dan/bai_cua_ban.sql`
