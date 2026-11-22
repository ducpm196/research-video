# Lab DVO L12 — Ký và xác minh chữ ký gói dựng bằng RSA đồ chơi + SHA-256 thật

Viết chương trình Python băm SHA-256 gói `b'release-v1.0'`, rút gọn `digest_int % 3233`, ký bằng khoá bí mật `d = 2753` trên `n = 61 * 53 = 3233`, rồi kiểm chứng lại bằng `e = 17`, in đúng 3 dòng:
1. `n=3233 e=17`
2. `sig_matches_digest=1`
3. `tamper_detected=1`

Chấm tự động:
```bash
bash labs/cham.sh DVO L12 duong_dan/bai_cua_ban.py
```
