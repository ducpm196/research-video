# Lab DSC L00 — Biến gây nhiễu trong dữ liệu quan sát vs ngẫu nhiên hoá

Đọc `stdin` `seen_n=<int> seen_c=<int> un_n=<int> un_c=<int> obs=<0|1>`. Tính hiệu chênh lệch quan sát và bật cờ cần phân chia ngẫu nhiên theo biến `obs`.

In 1 dòng: `obs_diff=<.2f> needs_randomization=<0|1>`.
Chấm tự động: `bash labs/cham.sh DSC L00 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
