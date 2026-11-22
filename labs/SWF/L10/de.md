# Lab SWF L10 — Đo hiệu năng thực nghiệm có khoảng tin cậy 95%

Viết chương trình Python với mẫu hiệu số thời gian `d = [12.0 + (i % 5 - 2) * 0.5 for i in range(30)]` (30 cặp đo): tính trung bình hiệu, độ lệch chuẩn mẫu `s`, sai số chuẩn `s/sqrt(30)` và khoảng tin cậy 95% xấp xỉ `mean +- 2.045 * SE`, in đúng 3 dòng:
1. `n=30 mean=12.00`
2. `sd=0.719 se=0.131`
3. `ci95=11.73,12.27`

Chấm tự động:
```bash
bash labs/cham.sh SWF L10 duong_dan/bai_cua_ban.py
```
