# Lab NET L06 — Bảng định tuyến khớp tiền tố dài nhất (LPM)

Đọc `stdin` `routes=<cidr:gw,...> ip1=<ip> ip2=<ip> merge=<cidr,cidr>`. Áp dụng LPM cho `ip1, ip2` và gộp 2 tiền tố liền kề.

In đúng 3 dòng: `dst_10_1_10_5=<gw>`, `dst_8_8_8_8=<gw>`, `collapsed_prefix=<cidr>`.
Chấm tự động: `bash labs/cham.sh NET L06 duong_dan/bai_cua_ban.py`
