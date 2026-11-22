# Lab SAR L06 — Mạch sẵn sàng song song so với nối tiếp (98% mỗi thành phần)

Hai thành phần độc lập có độ sẵn sàng `a = 0,98` mỗi nút. Tính độ sẵn sàng khi ghép song song (`1 - (1 - a)^2`), ghép nối tiếp (`a^2`) và tỉ số thời gian gián đoạn giữa nối tiếp với song song theo công thức `(1 - series) / (1 - parallel)` (làm tròn tới số nguyên gần nhất bằng `round`).

Định dạng đầu ra (3 dòng):
`parallel_pct=<2 chữ số>%`
`series_pct=<2 chữ số>%`
`downtime_ratio=<số>x`

Chấm tự động:
```bash
bash labs/cham.sh SAR L06 duong_dan/bai_cua_ban.py
```
