# Lab DSY L09 [Mô phỏng phân tán] — Cửa sổ tumbling 5 giây trên luồng event-time

Viết chương trình Python phân loại dấu thời gian `[1, 2, 3, 7, 8, 12]` vào các cửa sổ `[0,5), [5,10), [10,15)` (`ts // 5`), in đúng 3 dòng:
1. `win0_count=3`
2. `win1_count=2`
3. `win2_count=1`

Chấm tự động:
```bash
bash labs/cham.sh DSY L09 duong_dan/bai_cua_ban.py
```
