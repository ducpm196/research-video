# Lab GFX L06 — Tính tích vô hướng Lambert và thành phần bóng sáng Blinn-Phong

Cho vector pháp tuyến `n = (0.0, 0.6, 0.8)` và hướng đèn `l = (0.0, 0.8, 0.6)`. Tính trực tiếp tích vô hướng `max(0, sum(a*b))` cho ánh sáng khuếch tán, cùng độ sáng phản chiếu `(0.95)^64` và `(0.95)^128`.
In đúng 1 dòng `diffuse=... spec_s64=... spec_s128=...` (2 chữ số cho diffuse, 4 cho spec).

Chấm tự động:
```bash
bash labs/cham.sh GFX L06 duong_dan/bai_cua_ban.py
```
