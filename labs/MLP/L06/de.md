# Lab MLP L06 — Cây quyết định, Rừng ngẫu nhiên & chỉ số Gini

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): trên `make_classification(n_samples=400, n_features=12, n_informative=4, random_state=42)` chia 70/30 `stratify=y, random_state=42`, huấn luyện `DecisionTreeClassifier(random_state=42)` (không giới hạn sâu) và `RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42)`, in đúng 3 dòng:
1. `dt_train_acc=1.000`
2. `rf_test_acc=...`
3. `importances_sum=1.00`

Chấm tự động:
```bash
bash labs/cham.sh MLP L06 duong_dan/bai_cua_ban.py
```
