# Lab SDP L02 — Đóng gói và bảo toàn bất biến tài khoản số dư >= 0

Viết lớp Python `Account(balance=100)` với phương thức `withdraw(amt)` từ chối khi `amt > _balance` (ném `ValueError`) và `deposit(amt)` hợp lệ, kiểm thử rút `150` bị chặn và giữ nguyên `100`, in đúng 3 dòng:
1. `overdraw_blocked=1`
2. `balance_after_reject=100`
3. `balance_after_valid_40=60`

Chấm tự động:
```bash
bash labs/cham.sh SDP L02 duong_dan/bai_cua_ban.py
```
