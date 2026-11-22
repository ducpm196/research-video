# Lab MLP L04 — StratifiedKFold + GridSearchCV bọc quanh Pipeline

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): trên `make_classification(n_samples=300, n_features=8, random_state=42)` chia 80/20 `stratify=y, random_state=42`, chạy `GridSearchCV` 5-fold (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) cho `{'clf__C': [0.01, 0.1, 1.0, 10.0]}` scoring=`'f1'`, và kiểm đếm số mẫu dương trên từng fold của `y_train`, in đúng 3 dòng:
1. `best_c=...`
2. `cv_f1=...`
3. `equal_folds_positive=...` (`1` nếu 5 fold có cùng số lượng dương tuyệt đối, `0` nếu chênh 1 mẫu do tổng số dương của `y_train` không chia hết cho 5)

Chấm tự động:
```bash
bash labs/cham.sh MLP L04 duong_dan/bai_cua_ban.py
```
