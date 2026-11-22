# Lab DAN L02 — Nối bảng quan hệ một–nhiều (1–N) làm nhân dòng tổng đơn hàng

Dùng thư viện `sqlite3` trong bộ nhớ tạm (RAM), tạo bảng đơn hàng `(1, 120), (2, 80)` và bảng chi tiết dòng hàng `(1),(1),(1),(1),(2)` (quan hệ 1–N). So sánh tổng sai khi nối thẳng với tổng đúng trước khi nối.

Định dạng đầu ra:
`joined_wrong=<số> true_sum=<số>`

Chấm tự động:
```bash
bash labs/cham.sh DAN L02 duong_dan/bai_cua_ban.py
```
