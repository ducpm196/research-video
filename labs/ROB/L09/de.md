# Lab ROB L09 — Chấm điểm cửa sổ động DWA

Đọc `gx gy ox oy vmax|v0,w0;...` từ stdin (ví dụ `2.0 0.5 1.2 0.0 0.6|0.6,0.0;0.4,0.5;0.2,-0.6`). Tính `scores` và chọn cặp lớn nhất.
In đúng 1 dòng `scores=[...] best=(score, (v, w))`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Công thức chi tiết: với mỗi cặp `(v, w)`, tiến 1 giây `(x, y, th) = (v*cos(w), v*sin(w), w)`, tính `head = max(0.0, 1.0 - abs(atan2(gy-y, gx-x) - th)/pi)`, `clr = min(1.0, hypot(x-ox, y-oy))`, và điểm `round(0.4*head + 0.4*clr + 0.2*(v/vmax), 3)`.
