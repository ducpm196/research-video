# Lab MLP L00 — Pipeline chống rò rỉ dữ liệu trên dữ liệu bảng

Đọc cấu hình từ `stdin` (dạng `khoá=giá trị`, dùng `labs/.venv-ml`):
- `n_samples=<int> n_features=<int> test_size=<float> seed=<int>`
- `train_vals=<v1,v2,...> test_vals=<u1,...>`

Yêu cầu:
1. Sinh dữ liệu `make_classification(n_samples=n_samples, n_features=n_features, random_state=seed)`, chia phân tầng `train_test_split(..., test_size=test_size, stratify=y, random_state=seed)` và khớp `Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=seed))])`.
2. Trên mảng 1 cột `train_vals` vs `train_vals + test_vals`, đo `mean_[0]` của `StandardScaler` không rò rỉ (`clean_mean`) và có rò rỉ (`leak_mean`).

In đúng 3 dòng:
```
clean_mean=<.2f>
leak_mean=<.2f>
pipe_test_acc=<.3f>
```

Chấm tự động: `bash labs/cham.sh MLP L00 duong_dan/bai_cua_ban.py`
