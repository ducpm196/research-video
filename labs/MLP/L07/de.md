# Lab MLP L07 — Tăng cường độ dốc HistGradientBoosting & đối chứng cộng phần dư

Đọc từ `stdin`:
`n_samples=<int> n_features=<int> n_informative=<int> test_size=<float> seed=<int> max_iter=<int> lr=<float> res_steps=<int> target=<float>`

Yêu cầu: huấn luyện `HistGradientBoostingClassifier(max_iter=max_iter, learning_rate=lr, random_state=seed)` và chạy `res_steps` bước cộng phần dư từ `0.0` hướng tới `target` với tốc độ `lr`. In đúng 3 dòng: `n_iter=<int>`, `hgb_test_acc=<.3f>`, `res_after_3=<.3f>`.

Chấm tự động: `bash labs/cham.sh MLP L07 duong_dan/bai_cua_ban.py`
