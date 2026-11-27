# Lab DBS L15 — SQLite: SAVEPOINT và cô lập ngăn đọc bẩn

Cơ sở dữ liệu có sẵn `Gia(id, v)` và `Params(v0, v1, v2)`. Mở giao dịch (`BEGIN;`) cập nhật thành `v1`, chạy `SAVEPOINT s1;` rồi thử đổi sang `v2` và `ROLLBACK TO s1;` để lùi riêng thay đổi đó, đọc giá trị sau `s1`, sau đó chạy `ROLLBACK;` toàn giao dịch để khôi phục `v0`.

In đúng 3 dòng: `after_s1_rollback=<d>`, `after_full_rollback=<d>`, `dirty_read_prevented=<0|1>`.
Chấm tự động: `bash labs/cham.sh DBS L15 duong_dan/bai_cua_ban.sql`
