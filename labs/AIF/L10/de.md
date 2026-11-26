# Lab AIF L10 — Tìm kế hoạch đảo chồng 3 khối trên bàn T

Đọc `stdin` `init=<A:P,B:N,C:T> goal=<...>`. Dùng BFS tìm số bước tối thiểu chuyển từ trạng thái chồng khối `init` sang `goal`.

In 1 dòng: `init_bottom=<b1> goal_bottom=<b2> min_actions=<d>`.
Chấm tự động: `bash labs/cham.sh AIF L10 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
