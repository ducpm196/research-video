# Lab GFX L01 — Nhân ma trận thuần nhất 3×3 chứng minh biến đổi 2D không giao hoán

Dựng hai ma trận `3×3` đầy đủ: quay `R(90°)` và tịnh tiến `T(3, -1)`. Nhân lần lượt `(T * R) * [1, 2, 1]^T` và `(R * T) * [1, 2, 1]^T` rồi lấy hai toạ độ đầu `(x, y)` làm tròn thành số nguyên.
In đúng 1 dòng `T_after_R=(x, y) R_after_T=(x, y)`.

Chấm tự động:
```bash
bash labs/cham.sh GFX L01 duong_dan/bai_cua_ban.py
```
