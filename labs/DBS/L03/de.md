# Lab DBS L03 — SQLite: logic ba trị NULL và hàm tổng hợp

Cơ sở dữ liệu có sẵn bảng `SV(ten, lop)`. So sánh `COUNT(*)` vs `COUNT(lop)`, `WHERE lop = NULL` vs `WHERE lop IS NULL`, và đếm số nhóm có từ 2 sinh viên trở lên.

In đúng 3 dòng: `cnt_all=<d> cnt_col=<d>`, `eq_null=<d> is_null=<d>`, `having_ge2_groups=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L03 duong_dan/bai_cua_ban.sql`
