# Lab DEN L10 — Mẫu hộp thư đi nguyên tử trong SQLite

Dùng `sqlite3` (CSDL SQLite trong bộ nhớ) tạo hai bảng `orders(id TEXT)` và `outbox(id TEXT)`. Thử ghi `('O100')` vào `orders` rồi kích hoạt lỗi trước khi ghi `outbox` để hoàn tác (`ROLLBACK`); sau đó thực hiện giao dịch hợp lệ ghi cả hai bảng với `('O200')`.

Định dạng đầu ra (2 dòng):
`orders_after_tx=<danh sách id>`
`outbox_after_tx=<danh sách id>`

Chấm tự động:
```bash
bash labs/cham.sh DEN L10 duong_dan/bai_cua_ban.py
```
