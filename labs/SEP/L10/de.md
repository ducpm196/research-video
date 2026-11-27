# Lab SEP L10 — Đếm số gói chịu ảnh hưởng bắc cầu

Đọc `gốc|u:v1,v2;...` từ stdin (ví dụ `leftpad|leftpad:tpl,cli;tpl:web;web:app;cli:app;app:`), trong đó mỗi mục `u:v1,v2` cho biết khi `u` bị gỡ thì các gói `v1, v2` chịu ảnh hưởng trực tiếp. Lưu vào từ điển `rev` (`dict`), rồi khởi tạo danh sách chờ `stack = list(rev[root])` và tập kết quả `broken = set()`. Lặp khi `stack` còn phần tử: lấy một gói `p = stack.pop()`, nếu `p` chưa nằm trong `broken` (tránh đếm trùng nút chung) thì thêm `p` vào `broken` và nối tiếp `stack.extend(rev.get(p, []))`.
In đúng 1 dòng `broken_upstream=<int> pkgs=<danh sách đã sắp xếp sorted(broken)>`.
