# Lab DVO L11 — Tính toán dung lượng lưu trữ nhật ký (log) theo lưu lượng yêu cầu/giây (req/s)

Viết chương trình Python tính lượng nhật ký (theo hệ thập phân `1 GB = 10^9 B, 1 TB = 10^12 B`) khi phát sinh `1 000 yêu cầu/giây (req/s)`, mỗi dòng `1 000 B`, lưu giữ `30` ngày, in đúng 3 dòng:
1. `gb_per_day=86.4`
2. `tb_30_days=2.59`
3. `sampling_10pct_tb=0.26`

Chấm tự động:
```bash
bash labs/cham.sh DVO L11 duong_dan/bai_cua_ban.py
```
