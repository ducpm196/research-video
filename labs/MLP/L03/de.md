# Lab MLP L03 — Cân bằng ngưỡng Precision–Recall từ xác suất dự báo

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): huấn luyện `Pipeline` (`StandardScaler` + `LogisticRegression(random_state=42)`) trên `make_classification(n_samples=240, n_features=6, random_state=42)` chia 75/25 `stratify=y, random_state=42`, tính `Recall` tại ngưỡng `0.50` và `0.30`, in đúng 3 dòng:
1. `r_at_50=...`
2. `r_at_30=...`
3. `recall_monotone_non_decreasing=1`

Chấm tự động:
```bash
bash labs/cham.sh MLP L03 duong_dan/bai_cua_ban.py
```
