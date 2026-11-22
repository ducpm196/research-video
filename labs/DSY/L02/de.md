# Lab DSY L02 [Mô phỏng phân tán] — So sánh đồng hồ Vector (happens-before vs concurrent)

Viết hàm `rel(u, v)` trả `'before'`, `'after'` hoặc `'concurrent'`, kiểm tra `(1,0,0)` với `(2,0,1)` và `(2,0,1)` với `(1,2,0)`, in đúng 3 dòng:
1. `v100_vs_v201=before`
2. `v201_vs_v120=concurrent`
3. `partial_order_ok=1`

Chấm tự động:
```bash
bash labs/cham.sh DSY L02 duong_dan/bai_cua_ban.py
```
