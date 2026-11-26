# Lab MLP L05 — Xử lý lệch nhãn & đo PR-AUC / Brier Score

Đọc từ `stdin`:
`n_samples=<int> w_neg=<float> w_pos=<float> n_informative=<int> test_size=<float> seed=<int>`

Yêu cầu: tạo dữ liệu lệch nhãn `make_classification`, chia phân tầng và so sánh `LogisticRegression(random_state=seed)` thường với `class_weight='balanced'` trong `Pipeline(StandardScaler + LogisticRegression)`. In đúng 3 dòng: `balanced_recall_ge_raw=<0_hoặc_1>`, `balanced_pr_auc=<.3f>`, `balanced_brier=<.3f>`.

Chấm tự động: `bash labs/cham.sh MLP L05 duong_dan/bai_cua_ban.py`
