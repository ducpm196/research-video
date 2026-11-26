# Lab EVT L02 — Cô lập thông điệp độc vào kênh thư chết (DLQ)

Đọc `stdin` `total=<int> poison=<int> retries=<int>`. Xử lý tuần tự thông điệp `1..total`: thông điệp `poison` thử lại `retries` lần rồi đẩy vào `DLQ` để các phần tử sau tiếp tục.

In 3 dòng: `processed=<d>`, `dlq=<list>`, `poison_attempts=<d>`.
Chấm tự động: `bash labs/cham.sh EVT L02 duong_dan/bai_cua_ban.py`
