# Lab SAR L09 — Bảo toàn lũy đẳng giao dịch trên SQLite

Đọc `stdin` `init_bal=<int> amt=<int> key=<str> tries=<int>`. Dùng SQLite tạo `ledger` và `idem(k PRIMARY KEY)` thử trừ `amt` lặp `tries` lần với cùng `key`.

In 3 dòng: `tx_attempts=<d>`, `applied_once=<d>`, `final_balance=<d>`.
Chấm tự động: `bash labs/cham.sh SAR L09 duong_dan/bai_cua_ban.py`
