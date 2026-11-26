# Lab NET L12 — Đếm số vòng RTT tải trang HTML và N đối tượng qua HTTP

Đọc `stdin` `objs=<int>`. Tính số vòng RTT cho HTTP/1.0 không bền (`2 + objs * 2`) vs HTTP/1.1 keep-alive tuần tự (`2 + objs * 1`) và lượng RTT tiết kiệm.

In đúng 3 dòng: `http_nonpersistent_rtt=<d>`, `http_persistent_seq_rtt=<d>`, `saved_rtt=<d>`.
Chấm tự động: `bash labs/cham.sh NET L12 duong_dan/bai_cua_ban.py`
