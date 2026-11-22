# Lab NET L12 (Mô phỏng DNS & HTTP) — Đếm vòng đi về RTT tải trang HTML + 10 đối tượng

Viết chương trình Python tính số vòng đi về `RTT` cần thiết khi tải 1 trang HTML + 10 ảnh bằng: HTTP/1.0 không bền (`2 RTT/mục`) và HTTP/1.1 keep-alive (kết nối bền) tuần tự không đường ống, in đúng 3 dòng:
1. `http_nonpersistent_rtt=22`
2. `http_persistent_seq_rtt=12`
3. `saved_rtt=10`

Chấm tự động:
```bash
bash labs/cham.sh NET L12 duong_dan/bai_cua_ban.py
```
