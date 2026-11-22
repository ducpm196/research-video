# Lab SEC L03 — Ràng buộc thử sai OTP (mã dùng một lần) 6 chữ số & tính xác suất trúng

Viết chương trình Python tính xác suất trúng nếu kẻ tấn công được thử `3` lần trên `10^6` mã 6 chữ số so với thử tự do `500 000` lần khi không có giới hạn tần suất, in đúng 3 dòng:
1. `prob_3_tries=3e-06`
2. `prob_unbounded_500k=0.50`
3. `rate_limit_factor=166667x`

Chấm tự động:
```bash
bash labs/cham.sh SEC L03 duong_dan/bai_cua_ban.py
```
