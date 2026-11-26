# Lab DBS L05 — SQLite: đối chiếu tách không mất thông tin vs tách mất

Cơ sở dữ liệu có sẵn bảng `DK(mssv, lop, mon)`. Đếm số dòng gốc, số dòng khi chiếu tách đúng theo `mssv` rồi nối lại và số dòng ma sinh ra khi tách sai theo `lop`.

In đúng 3 dòng: `orig_rows=<d>`, `good_join_rows=<d>`, `bad_join_rows=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L05 duong_dan/bai_cua_ban.sql`
