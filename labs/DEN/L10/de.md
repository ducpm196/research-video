# Lab DEN L10 — Mẫu hộp thư đi nguyên tử trong SQLite

Đọc `stdin` `bad_id=<str> good_id=<str>`. Trong Python `sqlite3`: tạo kết nối `c = sqlite3.connect(':memory:')`, tạo hai bảng `orders(id TEXT)` và `outbox(id TEXT)` bằng `c.executescript(...)`, chèn `bad_id` vào `orders` bằng `c.execute('INSERT INTO orders VALUES(?)', (bad_id,))` rồi huỷ bằng `c.rollback()`. Sau đó chèn `good_id` vào cả `orders` và `outbox`, xác nhận bằng `c.commit()` và truy vấn danh sách `id` với `.fetchall()`.

In 2 dòng: `orders_after_tx=<list>`, `outbox_after_tx=<list>`.
Chấm tự động: `bash labs/cham.sh DEN L10 duong_dan/bai_cua_ban.py`
