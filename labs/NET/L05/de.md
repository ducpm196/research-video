# Lab NET L05 — Chia mạng con IPv4 và tính địa chỉ quảng bá

Đọc `stdin` `sub=<CIDR> parent=<CIDR> new_prefix=<int>`. Dùng thư viện chuẩn `ipaddress` lấy địa chỉ mạng, quảng bá, host dùng được của `sub` và số mạng con trong `parent`.

In đúng 3 dòng: `net=<ip> bcast=<ip>`, `usable_hosts=<d>`, `subnets_in_slash24=<d>`.
Chấm tự động: `bash labs/cham.sh NET L05 duong_dan/bai_cua_ban.py`
