# Lab OSY L04 (Mô phỏng đồng thời) — Duyệt mọi xen kẽ hai luồng tăng x++

Viết chương trình Python mô phỏng hai luồng, mỗi luồng thực hiện `x += 1` (gồm 3 bước `load, inc, store`) `2` lần từ `x = 0`. Duyệt tất cả chuỗi xen kẽ hợp lệ (tổng 12 bước = 6 của mỗi luồng), in đúng 3 dòng:
1. `possible_x=2,3,4`
2. `min_x=2 max_x=4`
3. `valid_outcomes_lt4=1`

Chấm tự động:
```bash
bash labs/cham.sh OSY L04 duong_dan/bai_cua_ban.py
```
