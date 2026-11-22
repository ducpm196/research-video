# Lab CAS L09 — Heartbleed (2014): kiểm đúng chuẩn RFC 6520 là 1 + 2 + payload_len + 16 <= record_len

Cài hàm kiểm tra bản ghi nhịp tim RFC 6520: hợp lệ khi `payload_len >= 0` và `1 + 2 + payload_len + 16 <= record_len` (1 byte loại + 2 byte độ dài + dữ liệu + 16 byte đệm tối thiểu). Kiểm tra hai gói: gói chuẩn `(payload=4, record_len=23)` và gói Heartbleed `(payload=65535, record_len=20)`.

Định dạng đầu ra (1 dòng):
`valid_ok=<0 hoặc 1> hb_ok=<0 hoặc 1> hb_overread_B=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh CAS L09 duong_dan/bai_cua_ban.py
```
