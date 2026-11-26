# Lab DBS L07 — SQLite: kiểm tra quét tuần tự SCAN trên bảng không chỉ mục

Cơ sở dữ liệu có sẵn bảng `Logs(id INT, code INT)` chưa tạo chỉ mục. Đếm tổng số dòng, xác nhận trong `sqlite_master` chưa có chỉ mục trên `Logs` và đếm số dòng có `code = 42`.

In đúng 3 dòng: `row_count=<d>`, `plan_uses_scan=<0|1>`, `hits_42=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L07 duong_dan/bai_cua_ban.sql`
