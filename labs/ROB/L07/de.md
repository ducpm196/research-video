# Lab ROB L07 — Đóng vòng đồ thị tư thế 1D

Đọc `loop_meas|p0,p1,...` từ stdin (ví dụ `3.5|0.0,1.0,2.0,3.0,4.0`). Phân bổ đều độ lệch `(loop_meas - raw[-1]) / len(raw)`.
In đúng 1 dòng `edge_corr=<3 chữ số> corrected_poses=[...]`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
