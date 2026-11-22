# Lab CAS L08 — GitLab (2017): tính thời gian chép khôi phục 240 GB ở 80 Mbps & khoá an toàn hostname

Kiểm tra cổng an toàn ngăn lệnh xoá chạy trên máy `'db-primary'` khi mục tiêu cho phép chỉ là `'db-secondary'`, đồng thời tính số giờ truyền khôi phục bản chụp `240 GB` qua mạng `80 Mbps` (`1 GB = 8 000 Mb`).

Định dạng đầu ra (1 dòng):
`aborted=<0 hoặc 1> restore_hours=<2 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CAS L08 duong_dan/bai_cua_ban.py
```
