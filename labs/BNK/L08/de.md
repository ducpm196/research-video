# Lab BNK L08 — Một giao dịch chốt, một giao dịch huỷ

Viết tệp `outbox.sql` (chạy bằng `python labs/sqlrun.py outbox.sql`, hoặc `sqlite3 :memory: < outbox.sql` nếu máy có `sqlite3`):

1. Tạo bảng `sodu (tk TEXT PRIMARY KEY, so_du INTEGER)` và `outbox (id INTEGER PRIMARY KEY, su_kien TEXT, da_gui INTEGER DEFAULT 0)`.
2. `INSERT INTO sodu VALUES ('B', 3000000);` rồi **`COMMIT;`** (để kết thúc giao dịch ngầm của câu `INSERT`).
3. Giao dịch 1 (`BEGIN; … COMMIT;`): trừ **700 000** ở `B` và thêm vào `outbox` sự kiện `'lenh 77 da tru 700000'`.
4. Giao dịch 2 (`BEGIN; … ROLLBACK;`): trừ **900 000** ở `B` và thêm sự kiện `'lenh 78 da tru 900000'`, rồi **huỷ**.
5. Hai câu `SELECT`: `so_du` của `sodu`; rồi `su_kien, da_gui` của `outbox`.

Chấm: `bash labs/cham.sh BNK L08 outbox.sql`.
