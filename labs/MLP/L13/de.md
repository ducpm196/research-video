# Lab MLP L13 — Tình huống chuyên gia: Phát hiện gian lận theo thời gian trên CPU

Đọc từ `stdin`:
`n_samples=<int> w_neg=<float> w_pos=<float> n_informative=<int> seed=<int> train_n=<int> max_iter=<int> lr=<float>`

Yêu cầu: cắt dữ liệu theo thời gian `[:train_n]` Train / `[train_n:]` Test, huấn luyện `HistGradientBoostingClassifier(max_iter=max_iter, learning_rate=lr, random_state=seed)` và so sánh PR-AUC với đường nền `0.0`. In đúng 3 dòng: `test_n=<int>`, `gb_pr_auc=<.3f>`, `beats_baseline=<0_hoặc_1>`.

Chấm tự động: `bash labs/cham.sh MLP L13 duong_dan/bai_cua_ban.py`
