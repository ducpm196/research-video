# Lab LNX L08 — Tách quy ước Ngoài:Trong và kiểm bất biến dữ liệu Volume theo stdin

Viết kịch bản Bash đọc `<host_port>:<container_port> <rows_count>` từ `stdin`, tách đúng `host_port` và `container_port`, mô phỏng giữ dữ liệu ổ gắn qua chu kỳ tạo lại trong thư mục tạm và in đúng 3 dòng: `host_port=... container_port=...`, `volume_persists=1`, `retained_rows=...`.

Chấm tự động:
```bash
bash labs/cham.sh LNX L08 duong_dan/bai_cua_ban.sh
```
