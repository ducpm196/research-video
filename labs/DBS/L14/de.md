# Lab DBS L14 — SQLite: mô phỏng WAL và pha REDO / UNDO

Cơ sở dữ liệu có sẵn bảng `WAL(lsn, tx, act, delta)` và bảng gốc một dòng `Base(v)`. Đếm số giao dịch đã `COMMIT` (REDO), chưa `COMMIT` (UNDO) và tính giá trị khôi phục cuối cùng.

In đúng 3 dòng: `redo_applied_tx=<d>`, `undo_reverted_tx=<d>`, `recovered_val=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L14 duong_dan/bai_cua_ban.sql`
