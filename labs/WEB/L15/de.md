# Lab WEB L15 — Node.js: so sánh độ trễ RTT từ HTTP/1.0 tới HTTP/2

Đọc `stdin` `rtt=<n> assets=<n>`. Tính độ trễ tải `1 HTML + assets ảnh` qua HTTP/1.0 (`2*(1+assets)` RTT), HTTP/1.1 nối tiếp 1 kết nối (`2 + assets` RTT) và HTTP/2 ghép kênh (`3` RTT).

In đúng 3 dòng: `http10_ms=<d>`, `http11_ms=<d>`, `http2_ms=<d>`.
Chấm tự động: `bash labs/cham.sh WEB L15 duong_dan/bai_cua_ban.js`
