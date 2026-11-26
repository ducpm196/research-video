# Lab DSY L03 — Kiểm tra mọi cặp tập đại biểu (R, W) trên N nút

Đọc `stdin` `n=<int> r_good=<int> w_good=<int> r_bad=<int> w_bad=<int>`. Kiểm vét cạn số cặp không giao nhau cho hai cấu hình `(R, W)` và tìm R tối thiểu khi W giữ bằng `w_bad` trên `5` nút.

In đúng 3 dòng: `quorum_2_2_all_intersect=<0|1>`, `pair_1_2_disjoint_cases=<d>`, `n5_min_r_when_w3=<d>` (tức `5 - w_bad + 1`).
Chấm tự động: `bash labs/cham.sh DSY L03 duong_dan/bai_cua_ban.py`
