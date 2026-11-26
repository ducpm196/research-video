# Lab DSY L09 — Cửa sổ tumbling theo kích thước cố định trên luồng event-time

Đọc `stdin` `win_s=<int> ts=<t1,t2,...>`. Đếm số sự kiện rơi vào 3 cửa sổ đầu `[0, W), [W, 2W), [2W, 3W)` theo `ts // win_s`.

In đúng 3 dòng: `win0_count=<d>`, `win1_count=<d>`, `win2_count=<d>`.
Chấm tự động: `bash labs/cham.sh DSY L09 duong_dan/bai_cua_ban.py`
