# Lab MLO L09 — Vòng phản hồi tự củng cố: top-2 chiếm dần lượt chọn

Đọc `stdin` `init=<c1,c2,...> rounds=<int> add=<int>`. Mỗi vòng chọn `2` mục cao nhất (hòa ưu tiên chỉ số nhỏ), cộng thêm `add` rồi tính tỉ lệ lượt bấm của 2 mục đầu.

In 1 dòng: `clicks=<list> top2_share=<.1f>%`.
Chấm tự động: `bash labs/cham.sh MLO L09 duong_dan/bai_cua_ban.py`
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
