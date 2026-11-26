# Lab MLP L08 — Đa thức bậc 2 trên hình tròn & kiểm chứng nhân quả TimeSeriesSplit

Đọc từ `stdin`:
`n_samples=<int> factor=<float> noise=<float> test_size=<float> seed=<int> degree=<int> ts_splits=<int> ts_len=<int>`

Yêu cầu: trên `make_circles(..., random_state=seed)` chia phân tầng `train_test_split(..., test_size=test_size, stratify=y, random_state=seed)`, so sánh `Pipeline([('sc', StandardScaler()), ('c', LogisticRegression(random_state=seed))])` thường với `Pipeline([('pf', PolynomialFeatures(degree=degree, include_bias=False)), ('sc', StandardScaler()), ('c', LogisticRegression(random_state=seed))])`. Đồng thời kiểm tra mọi fold của `TimeSeriesSplit(n_splits=ts_splits)` trên `np.arange(ts_len)` đều có `tr.max() < te.min()`.

In đúng 3 dòng: `linear_acc=<.3f>`, `poly2_acc=<.3f>`, `strict_causal_splits=<0_hoặc_1>`.
Chấm tự động: `bash labs/cham.sh MLP L08 duong_dan/bai_cua_ban.py`
