# Lab DSC L15 — Mốc 10%, cải thiện thực và độ lạc quan trộn

Đọc `stdin` `base=<float> ach=<float> ref=<float> k_params=<int> n_rows=<int>`. Tính mục tiêu giảm 10% (`floor(base * 0.9 * 10000) / 10000`, cắt 4 chữ số), phần trăm cải thiện `(base - ach) / base * 100`, khoảng lạc quan MSE `mgap = round(2 * k_params / (n_rows / 2), 5)` (làm tròn 5 chữ số thập phân) rồi đổi sang thước RMSE bằng `blend_opt = sqrt(ref**2 + mgap) - ref`.

In 1 dòng: `goal=<.4f> win_imp=<.2f>% blend_opt=<.5f>`.
Chấm tự động: `bash labs/cham.sh DSC L15 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
