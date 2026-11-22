# Lab SAR L09 — Bảo toàn lũy đẳng giao dịch trên cơ sở dữ liệu SQLite

Dùng `sqlite3` thật tạo bảng sổ cái `ledger(bal INT)` khởi tạo `400` và bảng khoá duy nhất `idem(k TEXT PRIMARY KEY)`. Chạy vòng lặp `3` lần thử trừ `125` với cùng khoá `'req-42'` trong cùng giao dịch `with conn:`, rồi in số lần thử, số lần ghi nhận đúng một lần và số dư cuối cùng.

Định dạng đầu ra (3 dòng):
`tx_attempts=<số>`
`applied_once=<số>`
`final_balance=<số>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L09 duong_dan/bai_cua_ban.py
```
