# Lab DSC L15 — Mốc 10%, cải thiện thực và độ lạc quan trộn

Đọc `stdin` `base=<float> ach=<float> ref=<float> k_params=<int> n_rows=<int>`. Tính mục tiêu giảm 10% (cắt 4 chữ số), phần trăm cải thiện và độ lạc quan từ `2 * k_params / (n_rows / 2)`.

In 1 dòng: `goal=<.4f> win_imp=<.2f>% blend_opt=<.5f>`.
Chấm tự động: `bash labs/cham.sh DSC L15 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
