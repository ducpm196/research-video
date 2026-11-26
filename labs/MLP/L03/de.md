# Lab MLP L03 — Cân bằng ngưỡng Precision–Recall từ xác suất dự báo

Đọc từ `stdin`:
`n_samples=<int> n_features=<int> test_size=<float> seed=<int> th_hi=<float> th_lo=<float>`

Yêu cầu: huấn luyện `Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=seed))])` trên `make_classification(..., random_state=seed)` chia phân tầng, tính `recall_score` trên tập Test ở `p >= th_hi` và `p >= th_lo`. In đúng 3 dòng: `r_at_50=<.3f>`, `r_at_30=<.3f>`, `recall_monotone_non_decreasing=<0_hoặc_1>`.

Chấm tự động: `bash labs/cham.sh MLP L03 duong_dan/bai_cua_ban.py`
