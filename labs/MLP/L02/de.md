# Lab MLP L02 — Hồi quy có điều chuẩn Ridge & Lasso chống quá khớp

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): dùng `make_regression(n_samples=150, n_features=12, n_informative=4, noise=2.0, random_state=42)`, xây `Pipeline` có `StandardScaler()` cho `Ridge(alpha=10.0)` và `Lasso(alpha=2.0)`, kiểm chứng mức co độ dài `||w||` khi tăng alpha từ 0.1 lên 100.0, in đúng 3 dòng:
1. `ridge_zero_coefs=...`
2. `lasso_zero_coefs=...`
3. `higher_alpha_shrinks=1`

Chấm tự động:
```bash
bash labs/cham.sh MLP L02 duong_dan/bai_cua_ban.py
```
