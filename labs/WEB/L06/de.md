# Lab WEB L06 — Node.js thật: kiểm chuẩn RFC 9110 phương thức HTTP và lũy đẳng

Viết bảng kiểm chuẩn các phương thức `GET, PUT, DELETE, POST` và mô phỏng Idempotency-Key chống trừ tiền 2 lần khi gửi lại `POST /pay`, in đúng 3 dòng:
1. `get_safe_idem=1,1`
2. `put_safe_idem=0,1`
3. `post_with_idem_key_bal=150`

Chấm tự động:
```bash
bash labs/cham.sh WEB L06 duong_dan/bai_cua_ban.js
```
