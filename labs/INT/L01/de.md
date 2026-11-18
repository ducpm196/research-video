# Lab INT L01 — Trả lời một câu phỏng vấn có số: chỉ mục B-Tree và bộ nhớ luồng (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, và `cham.sh` không chấm tệp `.md`. Tính tay, ghi từng dòng đúng định dạng dưới đây, rồi tự so với `loi_giai.md`.

Số liệu (số minh hoạ): bảng **80 000 000** dòng; mỗi nút chỉ mục chứa tối đa **500** nhánh; **2 000** tác vụ chờ vào ra cùng lúc; mỗi luồng hệ điều hành dự trữ **1 MB** ngăn xếp; mỗi luồng ảo khoảng **2 000 byte** (số minh hoạ, thực tế đổi theo độ sâu lời gọi).

Viết bốn dòng:
1. `chieu cao cay: <số>` — số tầng nhỏ nhất h sao cho 500^h ≥ 80 000 000.
2. `so lan doc mot dong: <số>` — h lần đọc trên cây cộng 1 lần đọc dòng dữ liệu.
3. `ngan xep luong he dieu hanh: <số> MB` — 2 000 × 1 MB.
4. `ngan xep luong ao: <số> byte` — 2 000 × 2 000 byte.

Tự kiểm bằng Python (không bắt buộc, sau khi đã tính tay): chạy `python -c "import math; print(math.ceil(math.log(80000000,500)), 2000*1, 2000*2000)"` rồi so với dòng 1, 3, 4 (dòng 2 bằng dòng 1 cộng 1).
