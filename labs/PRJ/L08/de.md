# Dự án PRJ L08 — Bộ đánh giá phân loại F1 & sai số hiệu chuẩn ECE

Đọc từ luồng chuẩn (`stdin`) 2 dòng:
- Dòng 1: `tp=<int> fp=<int> fn=<int>`
- Dòng 2: `bins=<n1,acc1,conf1;n2,acc2,conf2;...>` (số mẫu, độ chính xác thực tế và độ tự tin trung bình của từng giỏ)

Yêu cầu chương trình Python:
1. Tính `Precision = tp / (tp + fp)`, `Recall = tp / (tp + fn)`, `F1 = 2 * P * R / (P + R)`.
2. Tính `ECE = sum((n_b / N) * |acc_b - conf_b|)` với `N = sum(n_b)`.

In đúng 3 dòng (làm tròn 2 chữ số thập phân):
```
precision=<.2f> recall=<.2f>
f1=<.2f>
ece=<.2f>
```

Chấm tự động:
```bash
bash labs/cham.sh PRJ L08 duong_dan/bai_cua_ban.py
```
