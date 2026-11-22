# Lab MLP L00 — Pipeline chống rò rỉ dữ liệu trên dữ liệu bảng

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): (1) dùng `make_classification(n_samples=120, n_features=4, random_state=42)` chia `test_size=0.25, stratify=y, random_state=42`; (2) chạy `Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))])`; (3) kiểm `mean_` khi không rò rỉ trên `[0.0, 2.0]` vs có rò rỉ với `[10.0]`, in đúng 3 dòng:
1. `clean_mean=1.00`
2. `leak_mean=4.00`
3. `pipe_test_acc=...`

Chấm tự động:
```bash
bash labs/cham.sh MLP L00 duong_dan/bai_cua_ban.py
```
