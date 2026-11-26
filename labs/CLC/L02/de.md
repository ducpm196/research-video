# Lab CLC L02 — Chia mạng con trên VPC bằng thư viện ipaddress

Đọc `stdin` `vpc=<CIDR> new_prefix=<int> reserved=<int>`. Tách VPC thành các mạng con `/new_prefix`, đếm số mạng con, IP mỗi mạng và IP khả dụng sau khi trừ `reserved`.

In 3 dòng: `subnets_24=<d>`, `ips_per_24=<d>`, `usable_cloud_ips=<d>` (lưu ý: giữ nguyên tên khoá `subnets_24` và `ips_per_24` theo mẫu ngay cả khi `new_prefix` khác `24`).
Chấm tự động: `bash labs/cham.sh CLC L02 duong_dan/bai_cua_ban.py`
