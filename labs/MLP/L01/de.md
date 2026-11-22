# Lab MLP L01 — ColumnTransformer điền khuyết trung vị & mã hóa bỏ qua nhãn lạ

Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): cho Train `[[10.0,'hn'], [20.0,'sg'], [30.0,'hn'], [np.nan,'sg']]` và Test `[[np.nan,'dn']]`, dùng `ColumnTransformer` với `SimpleImputer(strategy='median')` cho cột `[0]` và `OneHotEncoder(handle_unknown='ignore')` cho cột `[1]`, in đúng 3 dòng:
1. `train_median=20.0`
2. `test_imputed_val=20.0`
3. `unknown_ohe_sum=0`

Chấm tự động:
```bash
bash labs/cham.sh MLP L01 duong_dan/bai_cua_ban.py
```
