# Lab MLP L06 — Cây quyết định, Rừng ngẫu nhiên & chỉ số Gini

Đọc từ `stdin`:
`n_samples=<int> n_features=<int> n_informative=<int> test_size=<float> seed=<int> n_estimators=<int> max_depth=<int>`

Yêu cầu: huấn luyện `DecisionTreeClassifier(random_state=seed)` và `RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=seed)`. In đúng 3 dòng: `dt_train_acc=<.3f>`, `rf_test_acc=<.3f>`, `importances_sum=<.2f>`.

Chấm tự động: `bash labs/cham.sh MLP L06 duong_dan/bai_cua_ban.py`
