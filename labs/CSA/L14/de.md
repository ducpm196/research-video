# Lab CSA L14 (Mô phỏng bộ nhớ ảo & TLB) — Dịch địa chỉ 4 KB (VPN -> khung vật lý) và tính EAT

Viết chương trình Python với trang `4 096 byte`, số trang ảo VPN `0x05` ánh xạ vào khung vật lý `0x12`, dịch địa chỉ ảo `0x5ABC` và tính thời gian truy cập hiệu dụng EAT khi `TLB hit = 98%` (TLB 1 ns, RAM 100 ns), in đúng 3 dòng:
1. `vpn=0x05 offset=0xABC`
2. `phys_addr=0x12ABC`
3. `eat_ns=103.00`

Chấm tự động:
```bash
bash labs/cham.sh CSA L14 duong_dan/bai_cua_ban.py
```
