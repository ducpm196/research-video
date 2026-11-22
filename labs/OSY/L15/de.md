# Lab OSY L15 (Mô phỏng bộ lập lịch Linux) — Đối chiếu O(n) vs CFS vs EEVDF

Viết chương trình Python mô phỏng tỉ trọng CPU giữa hai tác vụ trọng số `2048` và `1024` trong CFS, lượt duyệt của bộ lập lịch O(n) `1 000` tiến trình × `1 000` Hz, và lát cắt EEVDF `3 ms` vs `9 ms` trong chu kỳ `36 ms`, in đúng 3 dòng:
1. `on_checks_per_sec=1000000`
2. `cfs_share_2048_vs_1024=66.7%,33.3%`
3. `eevdf_ms_36ms=18,18 first=A`

Chấm tự động:
```bash
bash labs/cham.sh OSY L15 duong_dan/bai_cua_ban.py
```
