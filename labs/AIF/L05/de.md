# Lab AIF L05 — Thoả ràng buộc CSP: tô màu bản đồ

Đọc `stdin` chuỗi `n=<int> colors=<int> edges=<u:v,...>` trên đồ thị `n` đỉnh (`0..n-1`). Duyệt vét cạn toàn bộ gán màu đếm tổng phép gán `colors^n` và số nghiệm hợp lệ không trùng màu hai đầu cạnh.

In 1 dòng: `total_assign=<d> valid_solutions=<d>`.
Chấm tự động: `bash labs/cham.sh AIF L05 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
