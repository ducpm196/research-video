# Lab SDP L16 — Thiết kế lại giỏ hàng bằng Strategy

Viết hàm tính tiền giỏ hàng `[150000, 200000, 100000]` qua hai chiến lược: `pct10_over_300k` (giảm 10% nếu tổng > 300 000) và `flat_50k` (giảm thẳng 50 000), in đúng 3 dòng:
1. `subtotal=450000`
2. `pct10_total=405000`
3. `flat50_total=400000`

Chấm tự động:
```bash
bash labs/cham.sh SDP L16 duong_dan/bai_cua_ban.py
```
