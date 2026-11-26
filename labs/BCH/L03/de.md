# Lab BCH L03 — Chữ ký số trên mô hình RSA đồ chơi

Đọc `n e d|msg_orig|msg_test` từ stdin (ví dụ `3233 17 2753|A trả B 15|A trả B 150`). Chuyển mỗi thông điệp sang số nguyên bằng toàn bộ 64 chữ số hex SHA-256 UTF-8 (`int(sha256(msg.encode()).hexdigest(), 16) % n`), ký `msg_orig` thành `sig = pow(h_orig, d, n)` và kiểm định `pow(sig, e, n) == h(msg)` trên cả `msg_orig` lẫn `msg_test`.
In đúng 1 dòng `sig_valid=0/1 tampered_valid=0/1`.
