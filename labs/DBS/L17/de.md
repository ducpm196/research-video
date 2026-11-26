# Lab DBS L17 — SQLite: tính toán phân lô di chuyển bảng lớn không khoá lâu

Cơ sở dữ liệu có sẵn bảng cấu hình một dòng `Cfg(total_rows INT, batch_sz INT, sec_tenth INT, shadow_n INT)`. Tính số lô, tổng thời gian (giây) và chép `shadow_n` dòng đầu bằng `WITH RECURSIVE` sang bảng `Users_New`.

In đúng 3 dòng: `batches=<d>`, `total_seconds=<d>`, `shadow_copied=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L17 duong_dan/bai_cua_ban.sql`
