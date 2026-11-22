# Dự án PRJ L06 — Sổ nhật ký HMAC-SHA256 & chỉ mục SQLite

Viết chương trình Python tạo bảng SQLite có chỉ mục, chèn bản ghi `'pay:100'` kèm chữ ký HMAC-SHA256 (khoá `b'sec_key'`), kiểm tra truy vấn SQLi `' OR 1=1--` trả 0 dòng và chữ ký hợp lệ, in đúng 3 dòng:
1. `mac_len=64`
2. `sqli_blocked=1`
3. `hmac_verified=1`

Chấm tự động:
```bash
bash labs/cham.sh PRJ L06 duong_dan/bai_cua_ban.py
```
