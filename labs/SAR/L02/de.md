# Lab SAR L02 — Ước lượng yêu cầu mỗi giây (QPS) và băng thông ở cao điểm

Hệ thống có `4 000 000` người dùng hoạt động mỗi ngày (`DAU`), mỗi người phát `30` yêu cầu/ngày, kích thước trung bình `1,5 KB` (`1 500 byte`) mỗi yêu cầu. Tính `QPS` trung bình, `QPS` cao điểm (nhân `3x`) và băng thông đỉnh tính bằng `MB/giây`.

Định dạng đầu ra (3 dòng):
`avg_qps=<số>`
`peak_qps=<số>`
`peak_mb_per_s=<2 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L02 duong_dan/bai_cua_ban.py
```
