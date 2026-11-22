# Lab WEB L00 — Node.js thật: tính TTFB (thời gian trước byte đầu tiên) qua TCP + TLS + HTTP với RTT

Viết tập lệnh Node.js (`*.js`) tính thời gian trước byte đầu tiên TTFB qua 3 chặng (TCP, TLS, HTTP GET) ở `RTT = 50 ms` so với người dùng ở xa `RTT = 200 ms` cộng `4` lượt gọi API tuần tự, in đúng 3 dòng:
1. `ttfb_50ms=150`
2. `remote_200ms_4api=1400`
3. `roundtrips_handshake=3`

Chấm tự động:
```bash
bash labs/cham.sh WEB L00 duong_dan/bai_cua_ban.js
```
