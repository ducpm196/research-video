# Lab DBS L09 — SQLite: chỉ mục ghép cột (lop, diem) và quy tắc tiền tố trái

Cơ sở dữ liệu có sẵn bảng `Diem(id, lop, diem)`. Tạo chỉ mục ghép `idx_ld` trên `Diem(lop, diem)`, xác nhận chỉ mục tồn tại trong bảng hệ thống `sqlite_master` (`name='idx_ld'`), đếm sinh viên `lop='K1' AND diem >= 8` và tổng số dòng có `diem BETWEEN 7 AND 9`.

In đúng 3 dòng: `composite_idx_ok=<d>`, `k1_ge8=<d>`, `between_7_9=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L09 duong_dan/bai_cua_ban.sql`
