# Lab GFX L10 — Tính phản xạ Fresnel bằng xấp xỉ Schlick theo góc nhìn

Cho vật liệu điện môi có `F0 = 0.04`, tính tỉ lệ phản xạ tại ba góc `cos_theta in {1.0, 0.5, 0.1}` bằng công thức `F0 + (1 - F0)*(1 - cos_theta)^5`.
In đúng 1 dòng `F0=... F60=... F84=...` (3 chữ số).

Chấm tự động:
```bash
bash labs/cham.sh GFX L10 duong_dan/bai_cua_ban.py
```
