# Lab DBS L02 — SQLite: LEFT JOIN và bẫy lọc ở WHERE vs ON

Cơ sở dữ liệu có sẵn bảng `SV(ten, lop, diem)` và `Lop(ma, ten)`. Đếm dòng `LEFT JOIN` thuần, đếm khi lọc `WHERE Lop.ten='CS'`, và ghép danh sách tên điểm `>= 7` sắp xếp tăng dần theo tên (`ORDER BY ten`, dùng `COUNT(*)` và `GROUP_CONCAT(ten, ',')`).

In đúng 3 dòng: `left_all=<d>`, `left_where_drops_null=<d>`, `top_names=<danh_sach>`.
Chấm tự động: `bash labs/cham.sh DBS L02 duong_dan/bai_cua_ban.sql`
