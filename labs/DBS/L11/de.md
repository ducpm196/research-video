# Lab DBS L11 — SQLite: tính nguyên tử ACID với BEGIN, COMMIT và ROLLBACK

Cơ sở dữ liệu có sẵn bảng `TK(id, sd)` và bảng tham số một dòng `Params(xfer, abort_amt)`. Chạy giao dịch `COMMIT` chuyển `xfer` từ `'A'` sang `'B'`, rồi mở giao dịch thử trừ `abort_amt` ở `'A'` và gọi `ROLLBACK`.

In đúng 3 dòng: `after_commit=<A:..,B:..>`, `after_rollback=<A:..,B:..>`, `total_preserved=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L11 duong_dan/bai_cua_ban.sql`
