# Lab SDP L11 — Mẫu State: kiểm tra hợp lệ chuyển trạng thái đơn hàng

Viết bảng chuyển trạng thái đơn hàng (`NEW -> PAID -> SHIPPED`, `NEW -> CANCELLED`, `PAID -> CANCELLED`): đếm số cặp chuyển hợp lệ trong `3 x 3 = 9` cặp và xác nhận `SHIPPED -> CANCELLED` bị chặn, in đúng 3 dòng:
1. `valid_pairs=4`
2. `shipped_cancel_blocked=1`
3. `flow_end=SHIPPED`

Chấm tự động:
```bash
bash labs/cham.sh SDP L11 duong_dan/bai_cua_ban.py
```
