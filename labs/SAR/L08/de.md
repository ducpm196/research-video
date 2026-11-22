# Lab SAR L08 — Tính tồn đọng hàng đợi (backlog) và thời gian xả (drain)

Trong `30` phút cao điểm (`1 800` giây), nguồn gửi `250 thông điệp/giây` trong khi dịch vụ xử lý `200 thông điệp/giây`. Sau đó nguồn giảm xuống `140 thông điệp/giây`. Tính tổng tồn đọng tích lũy, tốc độ xả ròng và số phút xả sạch.

Định dạng đầu ra (3 dòng):
`backlog_30m=<số>`
`drain_net_per_s=<số>`
`drain_minutes=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L08 duong_dan/bai_cua_ban.py
```
