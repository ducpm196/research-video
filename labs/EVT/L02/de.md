# Lab EVT L02 — Cô lập thông điệp độc vào kênh thư chết (DLQ)

Mô phỏng vòng lặp tiêu thụ `500` thông điệp đánh số `1..500`, trong đó thông điệp `#7` luôn hỏng vĩnh viễn. Mỗi thông điệp hỏng được thử lại tối đa `3` lượt rồi đẩy sang kênh thư chết (`DLQ`) để các phần tử sau tiếp tục được xử lý.

Định dạng đầu ra (3 dòng):
`processed=<số nguyên>`
`dlq=<danh sách>`
`poison_attempts=<số lần thử của #7>`

Chấm tự động:
```bash
bash labs/cham.sh EVT L02 duong_dan/bai_cua_ban.py
```
