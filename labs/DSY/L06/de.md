# Lab DSY L06 — Băm modulo vs Băm nhất quán khi mở rộng cụm

Đọc `stdin` `keys=<int> n_old=<int> n_new=<int>`. Tính tỉ lệ khóa dịch chuyển với phép chia dư và với băm nhất quán SHA-256 dùng 100 nút ảo mỗi nút (khoá vòng `f"n{i}#{v}"` với `v` từ 0 tới 99, 8 hex đầu).

In đúng 3 dòng: `mod_moved_pct=<.1f>%`, `ch_moved_lt_30pct=<0|1>`, `ideal_moved_pct=<.1f>%`.
Chấm tự động: `bash labs/cham.sh DSY L06 duong_dan/bai_cua_ban.py`
