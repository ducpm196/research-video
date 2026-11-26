# Lab MLP L04 — StratifiedKFold + GridSearchCV bọc quanh Pipeline

Đọc từ `stdin`:
`n_samples=<int> n_features=<int> test_size=<float> seed=<int> n_splits=<int> c_grid=<c1,c2,...>`

Yêu cầu: chạy `GridSearchCV(pipe, {'clf__C': c_grid}, cv=StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed), scoring='f1')` trên `make_classification`, kiểm tra số mẫu dương ở từng fold của `y_tr` có bằng nhau tuyệt đối hay không. In đúng 3 dòng: `best_c=<float>`, `cv_f1=<.3f>`, `equal_folds_positive=<0_hoặc_1>`.

Chấm tự động: `bash labs/cham.sh MLP L04 duong_dan/bai_cua_ban.py`
