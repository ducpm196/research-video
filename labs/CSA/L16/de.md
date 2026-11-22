# Lab CSA L16 (Mô phỏng kiến trúc chuyên gia) — Đa nhân Amdahl và chênh lệch thời gian cache

Viết chương trình Python tính tăng tốc giới hạn của phần tuần tự `15%` khi mở rộng sang 8 nhân và mô phỏng độ trễ cache hit (`2 ns`) vs miss (`100 ns`) bộc lộ kênh kề, in đúng 3 dòng:
1. `speedup_8cores_p85=3.90`
2. `limit_inf=6.67`
3. `cache_timing_ratio=50.0x`

Chấm tự động:
```bash
bash labs/cham.sh CSA L16 duong_dan/bai_cua_ban.py
```
