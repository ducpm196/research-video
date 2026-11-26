# Lab WEB L06 — Node.js: kiểm chuẩn RFC 9110 phương thức HTTP và Idempotency-Key

Đọc `stdin` `bal=<n> keys=<k1:amt1,k2:amt2,...>`. Xuất chuẩn an toàn/lũy đẳng của `GET` và `PUT`, đồng thời chạy các giao dịch có `Idempotency-Key` để chống trừ tiền trùng lặp.

In đúng 3 dòng: `get_safe_idem=1,1`, `put_safe_idem=0,1`, `post_with_idem_key_bal=<d>`.
Chấm tự động: `bash labs/cham.sh WEB L06 duong_dan/bai_cua_ban.js`
