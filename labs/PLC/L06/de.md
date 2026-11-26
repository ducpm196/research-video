# Lab PLC L06 — Suy luận kiểu bằng hợp nhất ràng buộc

Đọc danh sách ràng buộc một chiều `lhs:rhs,...` từ `stdin` (ví dụ `ret:t_x,t_x:t_y,t_y:int`), trong đó `t_x`, `t_y`, `ret` là tên biến kiểu và các kiểu cơ bản gồm `int`, `bool`, `str`.
Gán `lhs` có kiểu theo `rhs` (`known[lhs] = known[rhs]`) và lặp giải thế bắc cầu tới khi không còn thay đổi để tìm kiểu cụ thể cho `t_x` và `ret`.

In đúng 1 dòng `inferred_tx=<kieu> ret=<kieu>`.
Chấm tự động: `bash labs/cham.sh PLC L06 duong_dan/bai_cua_ban.py`
