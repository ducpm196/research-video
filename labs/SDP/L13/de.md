# Lab SDP L13 — Tái cấu trúc an toàn: kiểm thử tương đương & ca biên

Đọc `stdin` `seed=<int> pairs=<int> edge_t=<int> edge_km=<int>`. Công thức chuẩn: thuế `t * 0.1`; phí giao `0` nếu `t >= 500000`, ngược lại `15000 + max(0, km - 5) * 4000`; tổng trả `round(t + thuế + phí giao)`. Dùng `r = random.Random(seed)` sinh `pairs` cặp `(r.randrange(0, 1000001, 1000), r.randrange(0, 31))` để đối chiếu hàm cũ với bản tái cấu trúc sạch và bản lỗi quên `max(0, km - 5)`.

In đúng 3 dòng: `new_mismatches=<d>`, `bug_mismatches=<d>`, `edge_500k_3km=<d>`.
Chấm tự động: `bash labs/cham.sh SDP L13 duong_dan/bai_cua_ban.py`
