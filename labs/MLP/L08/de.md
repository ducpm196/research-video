# Lab MLP L08 — Đa thức bậc 2 trên hình tròn & kiểm chứng nhân quả TimeSeriesSplit

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): so sánh `LogisticRegression` tuyến tính vs `PolynomialFeatures(degree=2, include_bias=False)` trên `make_circles(n_samples=300, factor=0.4, noise=0.05, random_state=42)` chia 70/30 `stratify=y, random_state=42`, và kiểm `TimeSeriesSplit(n_splits=4)` trên 100 chỉ số, in đúng 3 dòng:
1. `linear_acc=...`
2. `poly2_acc=1.000`
3. `strict_causal_splits=1`

Chấm tự động:
```bash
bash labs/cham.sh MLP L08 duong_dan/bai_cua_ban.py
```
