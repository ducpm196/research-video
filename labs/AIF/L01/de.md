# Lab AIF L01 — Tìm đường ngắn nhất BFS kiểm đích khi sinh nút

Đọc `stdin` `edges=<u:v1|v2,...> start=<S> goal=<G>`. Chạy BFS kiểm đích ngay lúc sinh nút kề để đếm khoảng cách ngắn nhất, số nút mở rộng và số nút đã thăm.

In 1 dòng: `shortest=<d> expanded=<d> visited=<d>`.
Chấm tự động: `bash labs/cham.sh AIF L01 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
