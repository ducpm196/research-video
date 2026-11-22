# Lab DEN L09 — Phát lại từ điểm kiểm tra khi dòng mới tiếp tục đổ vào

Khoảng cách giữa các điểm kiểm tra là `120` giây ở tốc độ nhận `8 000` sự kiện mỗi giây. Khi khởi động lại sau sự cố và xử lý ở công suất `24 000` sự kiện mỗi giây (trong khi dòng mới vẫn đến `8 000/s`), tính số sự kiện phải phát lại và thời gian đuổi kịp.

Định dạng đầu ra (2 dòng):
`replay_events=<số nguyên>`
`catchup_s=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh DEN L09 duong_dan/bai_cua_ban.py
```
