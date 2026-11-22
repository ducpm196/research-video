# Lab BCH L05 — Đào thử Bằng chứng Công việc PoW tìm SHA-256 mở đầu bằng '00'

Tăng `nonce` từ `0` trên chuỗi byte `f'khoi-99:{nonce}'.encode()` cho tới khi `hashlib.sha256(...).hexdigest()` bắt đầu bằng `'00'` (độ khó `8 bit 0`).
In đúng 1 dòng `found_nonce=... hash_prefix=...`.

Chấm tự động:
```bash
bash labs/cham.sh BCH L05 duong_dan/bai_cua_ban.py
```
