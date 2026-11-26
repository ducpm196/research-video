# Lab DEN L10 — Mẫu hộp thư đi nguyên tử trong SQLite

Đọc `stdin` `bad_id=<str> good_id=<str>`. Trong SQLite bộ nhớ, ghi `bad_id` vào `orders` rồi gọi `rollback()`, sau đó mở giao dịch ghi cả `orders` và `outbox` cho `good_id` rồi `commit()`.

In 2 dòng: `orders_after_tx=<list>`, `outbox_after_tx=<list>`.
Chấm tự động: `bash labs/cham.sh DEN L10 duong_dan/bai_cua_ban.py`
