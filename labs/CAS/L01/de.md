# Lab CAS L01 — Patriot (1991): sai số nhị phân 24-bit của 0.1 giây tích lũy sau 50h và 100h

Mô phỏng thanh ghi 24-bit (1 bit dấu + 23 bit phần lẻ, bước `scale = 1 << 23`) biểu diễn `1/10 = 0.1`: tính sai số chặt cụt mỗi tích tắc `0.1 - int(0.1 * scale)/scale`, rồi nhân với `50 giờ` và `100 giờ` ở tần số `10 Hz` (`0.1 giây/nhịp`).

Định dạng đầu ra (1 dòng):
`drift_50h=<4 chữ số> drift_100h=<4 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CAS L01 duong_dan/bai_cua_ban.py
```
