# Lab DBS L00 — SQLite: khoá chính (PK), khoá ngoại (FK) và toàn vẹn tham chiếu

Cơ sở dữ liệu khởi tạo sẵn hai bảng `Lop(ma)`, `SV(id, ten, lop REFERENCES Lop)` cùng bảng tạm `NhapSV(id, ten, lop)`. Viết tập lệnh SQLite bật `PRAGMA foreign_keys = ON;`, chèn bỏ qua trùng PK và chặn FK sai từ `NhapSV` (rồi thêm `(6,'Ha',NULL)`), xuất 3 dòng `sv_count`, `k9_blocked`, `null_fk_allowed`.

Chấm tự động: `bash labs/cham.sh DBS L00 duong_dan/bai_cua_ban.sql`
