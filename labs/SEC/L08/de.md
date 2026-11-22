# Lab SEC L08 — Tính và xác minh HMAC-SHA256 thật theo RFC 2104

Viết chương trình Python dùng `hmac.new` tính thẻ xác thực của thông điệp `b'chuyen 100'` với khoá `b'secret'`, kiểm tra đổi thành `b'chuyen 900'` làm chữ ký không khớp qua `hmac.compare_digest`, in đúng 3 dòng:
1. `mac_len_hex=64`
2. `orig_valid=1`
3. `tampered_valid=0`

Chấm tự động:
```bash
bash labs/cham.sh SEC L08 duong_dan/bai_cua_ban.py
```
