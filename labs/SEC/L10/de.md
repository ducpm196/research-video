# Lab SEC L10 — Tính ngưỡng 50% va chạm ngày sinh của hàm băm 64 bit

Viết chương trình Python tính số giá trị `k ≈ sqrt(2 * 2^64 * ln(2))` cần tạo để xác suất có ít nhất 1 cặp trùng nhau đạt `50%`, tính số bit bảo mật chống va chạm (`64 / 2 = 32` bit) và kiểm chứng bậc độ lớn của `k` tương đương ngưỡng tiền ảnh của hàm băm 32 bit (`round(k / 2^32) == 1`), in đúng 3 dòng:
1. `birthday_50pct_billions=5.06`
2. `bit_security_collision=32`
3. `ratio_vs_32bit_hash=1`

Chấm tự động:
```bash
bash labs/cham.sh SEC L10 duong_dan/bai_cua_ban.py
```
