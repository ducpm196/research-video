# Lab ESY L12 — Kiểm định watchdog timer và đo đỉnh ngăn xếp bằng mẫu 0xA5

Cho đồng hồ giám sát hết hạn ở `wdt_ms = 90 ms` chạy qua các chu kỳ `[50, 75, 110, 60]` ms (đếm số lần kích hoạt reset), và mô phỏng mảng ngăn xếp `16` byte tô kín `0xA5` bị ghi đè sâu `11` ô ở đáy.
In đúng 1 dòng `wdt_resets=... stack_used_B=...`.

Chấm tự động:
```bash
bash labs/cham.sh ESY L12 duong_dan/bai_cua_ban.py
```
