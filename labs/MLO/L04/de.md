# Lab MLO L04 — Quá khớp tập kiểm định khi thử nhiều cấu hình ngẫu nhiên

Đọc `stdin` `seed=<int> models=<int> samples=<int>`. Mô phỏng tất định `models` bộ đoán bừa đúng 50% trên `samples` mẫu và lấy điểm may mắn nhất.

In 1 dòng: `true_skill=0.50 best_lucky_val=<.2f>`.
Chấm tự động: `bash labs/cham.sh MLO L04 duong_dan/bai_cua_ban.py`
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Quy ước mô phỏng tung đồng xu: dùng `rng = random.Random(seed)` và tính mẫu đúng khi `rng.random() < 0.5`.
