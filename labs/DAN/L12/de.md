# Lab DAN L12 — Chia lệch & kiểm định lặp nhiều phiên bản

Đọc `stdin` `p_split=<float> alpha=<float> variants=<int> looks=<int>`. Tính hệ số chậm thời gian chạy khi chia lệch so với 50/50, cùng xác suất báo nhầm FWER với `variants` và `variants * looks`.

In 1 dòng: `split98_2_slow=<.2f>x fp4=<.1f>% fp20=<.1f>%`.
Chấm tự động: `bash labs/cham.sh DAN L12 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `kv = {k: float(v) for k, v in (t.split("=") for t in sys.stdin.read().split())}`; ép `int` cho `variants` và `looks`.
