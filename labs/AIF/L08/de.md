# Lab AIF L08 — Kiểm mô hình lôgic mệnh đề bằng liệt kê chân trị

Đọc `stdin` `req_c=<0|1> check_var=<A|B>`. Liệt kê 8 chân trị `(A, B, C)` thoả `KB = (not A or B) and (B or C) and (C == req_c)` và kiểm xem `KB` có kéo theo `check_var` không.

In 1 dòng: `kb_models=<d> entails_B=<0|1>`.
Chấm tự động: `bash labs/cham.sh AIF L08 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
