# Lab DBS L17 — SQLite: tính toán phân lô di chuyển bảng lớn không khoá lâu

Cơ sở dữ liệu có sẵn bảng cấu hình một dòng `Cfg(total_rows INT, batch_sz INT, sec_tenth INT, shadow_n INT)`. Tính số lô, tổng thời gian (giây) và chép `shadow_n` dòng đầu sang bảng mới bằng `CREATE TABLE Users_New(id INT); WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x < (SELECT shadow_n FROM Cfg)) INSERT INTO Users_New SELECT x FROM c;`.

In đúng 3 dòng: `batches=<d>`, `total_seconds=<d>`, `shadow_copied=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L17 duong_dan/bai_cua_ban.sql`
