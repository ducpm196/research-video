# Lab MLP L02 — Hồi quy có điều chuẩn Ridge & Lasso chống quá khớp

Đọc từ `stdin`:
`n_samples=<int> n_features=<int> n_informative=<int> noise=<float> seed=<int> r_low=<float> r_high=<float> lasso_alpha=<float>`

Yêu cầu: tạo dữ liệu bằng `make_regression(..., random_state=seed)`, chạy `Pipeline([('sc', StandardScaler()), ...])` cho `Ridge(alpha=r_low)`, `Ridge(alpha=r_high)` và `Lasso(alpha=lasso_alpha)` (đều `random_state=seed`), đếm số hệ số gần 0 (`|w| < 1e-6`) ở `Ridge(r_low)` và `Lasso(lasso_alpha)`, rồi kiểm tra `||w_high|| < ||w_low||`.

In đúng 3 dòng: `ridge_zero_coefs=<int>`, `lasso_zero_coefs=<int>`, `higher_alpha_shrinks=<0_hoặc_1>`.

Chấm tự động: `bash labs/cham.sh MLP L02 duong_dan/bai_cua_ban.py`
