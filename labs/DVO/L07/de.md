# Lab DVO L07 (Mô phỏng Canary) — Tính tỉ lệ lỗi canary và xác suất p nhị thức

Viết chương trình Python cho canary `1 000` yêu cầu gặp `20` lỗi trong khi nền lỗi cũ `p = 0.01`: tính số lỗi kỳ vọng (`10`), xác suất đuôi `P(X >= 20)` dưới `Binomial(1000, 0.01)` để ra quyết định rollback, in đúng 3 dòng:
1. `expected_errors=10`
2. `tail_prob_ge20=0.0033`
3. `rollback_triggered=1`

Chấm tự động:
```bash
bash labs/cham.sh DVO L07 duong_dan/bai_cua_ban.py
```
