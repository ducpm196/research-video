# Lab NET L11 — Tắc nghẽn TCP: quỹ đạo Slow Start, AIMD và Timeout

Đọc `stdin` `cwnd0=<int> ssthresh=<int> steps=<int>`. Mô phỏng `steps` RTT tăng gấp đôi khi `< ssthresh` và cộng 1 khi `>= ssthresh`, rồi gán trạng thái timeout.

In đúng 3 dòng: `slowstart_trace=<csv>`, `aimd_step1=<d>`, `after_timeout_ssthresh=<d> cwnd=1`.
Chấm tự động: `bash labs/cham.sh NET L11 duong_dan/bai_cua_ban.py`
