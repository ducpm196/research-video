# Lab MLP L13 — Tình huống chuyên gia: Phát hiện gian lận theo thời gian trên CPU

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): trên `make_classification(n_samples=1000, weights=[0.96, 0.04], n_informative=6, random_state=42)` cắt thời gian `[:750]` Train / `[750:]` Test, huấn luyện `HistGradientBoostingClassifier(max_iter=50, learning_rate=0.1, random_state=42)` và so sánh `PR-AUC` với đường nền `0.0`, in đúng 3 dòng:
1. `test_n=250`
2. `gb_pr_auc=...`
3. `beats_baseline=1`

Chấm tự động:
```bash
bash labs/cham.sh MLP L13 duong_dan/bai_cua_ban.py
```
