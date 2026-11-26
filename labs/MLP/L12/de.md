# Lab MLP L12 — Xuất mô hình JSON an toàn & đối chiếu sai số suy luận thuần

Đọc từ `stdin`:
`n_samples=<int> n_features=<int> seed=<int> check_n=<int>`

Yêu cầu: khớp `Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=seed))])`, xuất `mean, scale, w, b` qua `json.loads(json.dumps(...))`, kiểm công thức sigmoid thuần trên `check_n` mẫu đầu so với `predict_proba` (ngưỡng `1e-9`). In đúng 3 dòng: `json_keys_ok=<0_hoặc_1>`, `match_lt_1e9=<0_hoặc_1>`, `first_prob=<.6f>`.

Chấm tự động: `bash labs/cham.sh MLP L12 duong_dan/bai_cua_ban.py`
