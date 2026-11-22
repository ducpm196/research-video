# Lab CSA L10 (Mô phỏng phân cấp bộ nhớ) — Tính thời gian truy cập trung bình AMAT

Viết chương trình Python tính AMAT cho phân cấp L1 (`hit = 1 ns`, tỉ lệ trượt `5%`) → L2 (`hit = 10 ns`, tỉ lệ trượt cục bộ `20%`) → RAM (`100 ns`), in đúng 3 dòng:
1. `l2_amat_ns=30.0`
2. `total_amat_ns=2.50`
3. `locality_speedup_vs_ram=40.0`

Chấm tự động:
```bash
bash labs/cham.sh CSA L10 duong_dan/bai_cua_ban.py
```
