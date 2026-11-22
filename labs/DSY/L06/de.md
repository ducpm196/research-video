# Lab DSY L06 [Mô phỏng phân tán] — Băm modulo vs Băm nhất quán trên 1 000 khoá

Viết chương trình Python ánh xạ `1 000` khoá `0..999` khi cụm tăng từ `4` lên `5` nút: tính tỉ lệ khoá đổi nút với `k % N` vs băm nhất quán dùng SHA-256 trên vòng `[0, 2^32)`, in đúng 3 dòng:
1. `mod_moved_pct=80.0%`
2. `ch_moved_lt_30pct=1`
3. `ideal_moved_pct=20.0%`

Chấm tự động:
```bash
bash labs/cham.sh DSY L06 duong_dan/bai_cua_ban.py
```
