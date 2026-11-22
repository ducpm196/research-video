# Lab ESY L07 — Tính thông lượng và thời gian truyền khung UART 8N1 ở 9600 baud

Khung UART `8N1` cần `10` bit (`1 start + 8 data + 1 stop`) cho mỗi byte. Ở tốc độ `9600 baud`, tính số byte tối đa mỗi giây và thời gian truyền gói `24` byte (tính bằng `ms`).
In đúng 1 dòng `bytes_per_sec=... tx_24B_ms=...` (1 chữ số cho ms).

Chấm tự động:
```bash
bash labs/cham.sh ESY L07 duong_dan/bai_cua_ban.py
```
