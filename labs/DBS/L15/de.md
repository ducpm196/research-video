# Lab DBS L15 — SQLite: SAVEPOINT và cô lập ngăn đọc bẩn

Cơ sở dữ liệu có sẵn `Gia(id, v)` và `Params(v1, v2)`. Mở giao dịch cập nhật thành `v1`, tạo `SAVEPOINT s1`, thử đổi sang `v2` rồi `ROLLBACK TO s1`, đọc kết quả, sau đó `ROLLBACK` hoàn toàn và kiểm tra khôi phục giá trị gốc.

In đúng 3 dòng: `after_s1_rollback=<d>`, `after_full_rollback=<d>`, `dirty_read_prevented=<0|1>`.
Chấm tự động: `bash labs/cham.sh DBS L15 duong_dan/bai_cua_ban.sql`
