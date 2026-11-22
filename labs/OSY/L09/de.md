# Lab OSY L09 (Mô phỏng phân trang) — Dịch địa chỉ ảo (VPN + offset) và thời gian truy cập hiệu dụng EAT với TLB

Viết chương trình Python cho trang `4 KiB` (`4 096 B`), bảng trang `{0: 5, 1: 2, 2: 9, 3: 7}`, dịch địa chỉ `0x3A7F` và tính EAT khi `TLB=20 ns`, `RAM=100 ns`, `TLB hit=90%`, in đúng 3 dòng:
1. `va=0x3A7F vpn=3 offset=0xA7F`
2. `pa=0x7A7F`
3. `eat_ns=130.0`

Chấm tự động:
```bash
bash labs/cham.sh OSY L09 duong_dan/bai_cua_ban.py
```
