# Lab SEC L01 — PBKDF2-HMAC-SHA256 thật + tính thời gian vét cạn

Viết chương trình Python dùng `hashlib.pbkdf2_hmac` dẫn xuất khoá 32 byte dạng chuỗi hệ 16 (`hex`, 64 ký tự) từ `b'pw'` với muối ngẫu nhiên (`salt`) `b'salt1'` qua `10 000` vòng, đồng thời tính thời gian thử `26^8` mật khẩu ở tốc độ nhanh `1e10/s` vs chậm `1e4/s`, in đúng 3 dòng:
1. `fast_crack_s=20.9`
2. `slow_crack_days=242`
3. `pbkdf2_hex_len=64`

Chấm tự động:
```bash
bash labs/cham.sh SEC L01 duong_dan/bai_cua_ban.py
```
