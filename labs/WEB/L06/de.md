# Lab WEB L06 — Node.js: kiểm chuẩn RFC 9110 phương thức HTTP và Idempotency-Key

Đọc `stdin` `bal=<n> keys=<k1:amt1,k2:amt2,...>`. Xuất chuẩn an toàn/lũy đẳng của `GET` và `PUT`, đồng thời chạy các giao dịch có `Idempotency-Key` để chống trừ tiền trùng lặp.

Khung đọc `stdin` Node có sẵn: `const fs = require('fs'); const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')));` — duyệt `kv.keys.split(',')`, tách `k:amt` rồi kiểm tra khoá bằng `const seen = new Set();` (`seen.has(k)`, `seen.add(k)`), cập nhật số dư từ `Number(kv.bal)` và in 3 dòng bằng `console.log(...)`.

In đúng 3 dòng: `get_safe_idem=<0|1>,<0|1>`, `put_safe_idem=<0|1>,<0|1>`, `post_with_idem_key_bal=<d>`.
Chấm tự động: `bash labs/cham.sh WEB L06 duong_dan/bai_cua_ban.js`
