# Lab OSY L06 (Mô phỏng bế tắc) — Phát hiện chu trình Coffman và phá thứ tự khóa

Viết chương trình Python dựng đồ thị chờ giữa `5` triết gia (`0..4`) và `5` chiếc đũa (`0..4`): khi ai cũng cầm đũa trái trước tạo 1 chu trình độ dài 5, còn khi đánh số và luôn cầm đũa nhỏ trước sẽ phá vòng chờ, in đúng 3 dòng:
1. `naive_cycle_len=5`
2. `ordered_cycle=0`
3. `coffman_broken=circular_wait`

Chấm tự động:
```bash
bash labs/cham.sh OSY L06 duong_dan/bai_cua_ban.py
```
