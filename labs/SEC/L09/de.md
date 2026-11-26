# Lab SEC L09 — Ký chứng chỉ RSA đồ chơi và kiểm chứng khớp tên miền

Đọc `stdin` `signed=<domain> presented=<domain> bad=<domain>`. Dùng hàm băm rút gọn `h(s) = sum(s.encode()) % 30 + 2` và cặp khóa RSA đồ chơi modulo `n = 33` (`e = 3, d = 7`), tính chữ ký `sig = pow(h(signed), d, n)` và khôi phục `rec = pow(sig, e, n)` rồi kiểm chứng khớp `h(presented)` và `h(bad)`.

In đúng 3 dòng: `legit_cert_valid=<0|1>`, `forged_domain_valid=<0|1>`, `chain_verified=<0|1>`.
Chấm tự động: `bash labs/cham.sh SEC L09 duong_dan/bai_cua_ban.py`
