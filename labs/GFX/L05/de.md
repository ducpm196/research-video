# Lab GFX L05 — Tính bước lượng tử bộ đệm độ sâu 24-bit từ công thức đạo hàm d_n

Cho `far = 2000.0 m`, khoảng cách vật `z = 200.0 m` và độ sâu `24 bit`. Dùng công thức đạo hàm chính xác `dz = (z^2 * (f - n)) / (f * n * 2^24)` để tính bước phân giải nhỏ nhất (đổi ra `mm`) ở hai cấu hình `near = 0.1 m` và `near = 1.0 m`, cùng tỉ số cải thiện `gain`.
In đúng 1 dòng `dz_n01_mm=... dz_n10_mm=... gain=...x` (`2` chữ số thập phân cho `dz`, `1` chữ số cho `gain`).

Chấm tự động:
```bash
bash labs/cham.sh GFX L05 duong_dan/bai_cua_ban.py
```
