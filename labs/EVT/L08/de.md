# Lab EVT L08 — Tốc độ tăng độ trễ và thời gian xả tồn đọng

Dịch vụ nhận `900` sự kiện mỗi giây trong khi bộ tiêu thụ chỉ xử lý `750` mỗi giây suốt `1` giờ (`3600` giây). Sau đó tăng năng lực xử lý lên `1 200` sự kiện mỗi giây (trong khi vẫn nhận `900/s`), tính số tồn sau 1 giờ và thời gian xả hết tồn.

Định dạng đầu ra (2 dòng):
`backlog_1h=<số nguyên>`
`drain_s=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh EVT L08 duong_dan/bai_cua_ban.py
```
