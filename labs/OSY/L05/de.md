# Lab OSY L05 (Mô phỏng đồng bộ) — Semaphore sản xuất–tiêu thụ trên bộ đệm 5 ô

Viết chương trình Python mô phỏng bộ đệm `N = 5` bắt đầu `(empty=5, full=0)`: sản xuất `4` phần tử, tiêu thụ `1` phần tử, rồi sản xuất thêm `2` phần tử, in đúng 3 dòng:
1. `init_empty=5 init_full=0`
2. `after_4p_1c=empty:2,full:3`
3. `final_state=empty:0,full:5`

Chấm tự động:
```bash
bash labs/cham.sh OSY L05 duong_dan/bai_cua_ban.py
```
