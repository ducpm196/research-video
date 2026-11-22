# Lab MLP L05 — Xử lý lệch nhãn 5% & đo PR-AUC / Brier Score

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): trên `make_classification(n_samples=600, weights=[0.95, 0.05], n_informative=4, random_state=42)` chia 75/25 `stratify=y, random_state=42`, so sánh `LogisticRegression(random_state=42)` thường với `LogisticRegression(class_weight='balanced', random_state=42)` trong `Pipeline`, in đúng 3 dòng:
1. `balanced_recall_ge_raw=1`
2. `balanced_pr_auc=...`
3. `balanced_brier=...`

Chấm tự động:
```bash
bash labs/cham.sh MLP L05 duong_dan/bai_cua_ban.py
```
