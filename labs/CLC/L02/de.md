# Lab CLC L02 — Chia mạng con trên mạng ảo riêng (VPC) bằng thư viện ipaddress

Dùng thư viện chuẩn `ipaddress` chia mạng ảo riêng (`VPC`) dải `172.16.0.0/20` thành các mạng con (`subnet`) `/24`. Đếm tổng số mạng con `/24`, số địa chỉ IP mỗi mạng con và số IP khả dụng cho máy ảo sau khi trừ `5` địa chỉ nhà cung cấp giữ.

Định dạng đầu ra (3 dòng):
`subnets_24=<số>`
`ips_per_24=<số>`
`usable_cloud_ips=<số>`

Chấm tự động:
```bash
bash labs/cham.sh CLC L02 duong_dan/bai_cua_ban.py
```
