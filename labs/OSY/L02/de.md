# Lab OSY L02 — Lập lịch CPU: so sánh FCFS và SJF

Đọc `stdin` `bursts=<int,...>`. Tính thời gian chờ từng tiến trình và trung bình theo FCFS (đúng thứ tự đến) và SJF (việc ngắn nhất trước; mảng `sjf_waits` in lại theo đúng thứ tự tiến trình ban đầu `P1..Pn`), cùng lượng tiết kiệm `fcfs_avg - sjf_avg`.

In đúng 3 dòng (`<csv>` là các số cách nhau dấu phẩy, `<.2f>` là 2 chữ số thập phân): `fcfs_waits=<csv> avg=<.2f>`, `sjf_waits=<csv> avg=<.2f>`, `wait_saved=<.2f>`.
Chấm tự động: `bash labs/cham.sh OSY L02 duong_dan/bai_cua_ban.py`
