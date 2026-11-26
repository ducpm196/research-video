# Lab ROB L13 — Cột mốc Grand Challenge & quãng dừng mph

Đọc `d2004 pct d2005 v1_mph v2_mph` từ stdin (ví dụ `142 0.05 132 20.0 30.0`). Tính quãng hoàn thành và tỉ số quãng dừng.
In đúng 1 dòng `mi_2004=<1 chữ số> mi_2005=<int> stop_ratio=<2 chữ số>x`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Tham số cố định dùng cho tỉ số quãng dừng: `1 mph = 0.44704 m/s`, thời gian trễ `t = 0.2 s` và gia tốc phanh `a = 4.0 m/s^2`.
