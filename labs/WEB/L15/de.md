# Lab WEB L15 — Node.js thật: so sánh độ trễ RTT từ HTTP/1.0 tới HTTP/2 và HTTP/3

Viết tập lệnh Node.js tính độ trễ tải `1 HTML + 10 ảnh` ở `RTT = 50 ms` bằng HTTP/1.0 (`22` RTT), HTTP/1.1 keep-alive 1 kết nối tuần tự (`12` RTT), và HTTP/2 ghép kênh (`3` RTT), in đúng 3 dòng:
1. `http10_ms=1100`
2. `http11_ms=600`
3. `http2_ms=150`

Chấm tự động:
```bash
bash labs/cham.sh WEB L15 duong_dan/bai_cua_ban.js
```
