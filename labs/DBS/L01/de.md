# Lab DBS L01 — SQLite: CROSS JOIN vs INNER JOIN

Cơ sở dữ liệu có sẵn bảng `SV(id, ten, lop, diem)` và `Lop(ma, ten)`. Viết các truy vấn đếm số dòng `CROSS JOIN`, `INNER JOIN` theo `lop=ma`, và tìm tên sinh viên đầu tiên theo thứ tự chữ cái thuộc lớp `'CS'` đạt `diem >= 7` (gợi ý nối chuỗi bằng `||` và bọc `top_cs` bằng `COALESCE((SELECT ... ORDER BY SV.ten LIMIT 1), 'NONE')`).

In đúng 3 dòng: `cross_rows=<d>`, `inner_rows=<d>`, `top_cs=<ten>`.
Chấm tự động: `bash labs/cham.sh DBS L01 duong_dan/bai_cua_ban.sql`
