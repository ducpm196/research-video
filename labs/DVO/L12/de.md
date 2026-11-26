# Lab DVO L12 — Ký và xác minh chữ ký gói dựng bằng RSA + SHA-256

Đọc `stdin` `good=<str> tampered=<str>` (tuỳ chọn `d=<int>`, mặc định `2753`). Băm SHA-256 rút gọn modulo `n = 3233`, ký bằng khóa bí mật `d`, xác minh bằng `e = 17` và phát hiện gói bị sửa đổi.

In đúng 3 dòng: `n=3233 e=17`, `sig_matches_digest=<0|1>`, `tamper_detected=<0|1>`.
Chấm tự động: `bash labs/cham.sh DVO L12 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
