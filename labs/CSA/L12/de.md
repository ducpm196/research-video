# Lab CSA L12 (Mô phỏng Cache 2 đường LRU) — So sánh giảm conflict miss so với ánh xạ trực tiếp

Viết chương trình Python mô phỏng cache 2-way (mỗi set 2 slot, LRU) giải cùng chuỗi ping-pong hai địa chỉ ánh xạ cùng set `idx = 0`: `[0x00, 0x80, 0x00, 0x80]`, in đúng 3 dòng:
1. `direct_mapped_hits=0 misses=4`
2. `two_way_lru_hits=2 misses=2`
3. `final_set0_order=0x00,0x80`

Chấm tự động:
```bash
bash labs/cham.sh CSA L12 duong_dan/bai_cua_ban.py
```
