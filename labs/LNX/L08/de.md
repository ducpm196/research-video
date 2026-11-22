# Lab LNX L08 — Kiểm chứng quy ước Ngoài:Trong và bất biến bảo toàn dữ liệu Volume

Viết kịch bản Bash kiểm tra phân tách chuỗi cổng/ổ gắn theo quy ước `Ngoài:Trong` và bất biến bảo toàn dữ liệu qua vòng đời container để in đúng 3 dòng:
1. `host_port=8080 container_port=80`
2. `volume_persists=1`
3. `retained_rows=500`

Chấm tự động:
```bash
bash labs/cham.sh LNX L08 duong_dan/bai_cua_ban.sh
```
