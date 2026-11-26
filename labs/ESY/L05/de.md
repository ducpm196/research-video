# Lab ESY L05 — Lọc bậc nhất và công thức đóng

Đọc `alpha x steps` từ stdin (ví dụ `0.25 1.0 8`). Khởi tạo `y = 0.0`, lặp `steps` bước `y += alpha * (x - y)` và đối chiếu công thức đóng tổng quát `x * (1 - (1 - alpha) ** steps)`.
In đúng 1 dòng `y8=<4 chữ số> closed_form=<4 chữ số>` (luôn giữ nguyên tên khoá `y8=` cho mọi giá trị `steps`).
