# Lab SEP L10 — Đếm số gói chịu ảnh hưởng bắc cầu

Đọc `gốc|u:v1,v2;...` từ stdin (ví dụ `leftpad|leftpad:tpl,cli;tpl:web;web:app;cli:app;app:`). Duyệt đồ thị phụ thuộc bằng ngăn xếp DFS (hoặc hàng đợi BFS: khởi tạo `stack = list(rev[root])`, `broken = set()`, lặp lấy phần tử chưa thăm thêm các gói phụ thuộc tiếp theo) tìm tất cả gói phụ thuộc trực tiếp hoặc bắc cầu vào gói gốc.
In đúng 1 dòng `broken_upstream=<int> pkgs=<danh sách sắp xếp>`.
