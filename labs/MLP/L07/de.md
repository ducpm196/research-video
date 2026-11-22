# Lab MLP L07 — Tăng cường độ dốc HistGradientBoosting & đối chứng cộng phần dư

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): chạy `HistGradientBoostingClassifier(max_iter=50, learning_rate=0.1, random_state=42)` trên `make_classification(n_samples=600, n_features=12, n_informative=6, random_state=42)` chia 75/25 `stratify=y, random_state=42`, kèm 3 bước cộng phần dư từ `0.0` tới `10.0` với `lr=0.1`, in đúng 3 dòng:
1. `n_iter=50`
2. `hgb_test_acc=...`
3. `res_after_3=7.290`

Chấm tự động:
```bash
bash labs/cham.sh MLP L07 duong_dan/bai_cua_ban.py
```
