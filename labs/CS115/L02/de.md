# Lab CS115 L02 — Nhân ma trận và giải M w = b

Cần: Python 3 (không cần thư viện ngoài). Tạo tệp `matran.py`. Ma trận viết bằng danh sách các hàng, ví dụ `[[2, 0], [1, 3]]` (số minh hoạ, khác ví dụ trong bài).

1. Viết hàm `nhan(A, B)` nhân hai ma trận (ô hàng i, cột j = hàng i của A nhân cột j của B). Với `A = [[2, 0], [1, 3]]`, `B = [[1, 4], [2, 5]]` in `AB = ...`, `BA = ...` và `AB khac BA: True`.
2. Với `M = [[3, 1], [5, 2]]`, `b = [13, 22]`: in `dinh thuc M: <ad - bc>`, nghịch đảo `M nghich dao: ...` (đổi chỗ a và d, đổi dấu b và c, chia cho định thức; dùng `Fraction` rồi in từng số bằng `str`), nghiệm `w = [...]` (nghịch đảo nhân b) và kiểm tra lại `M.w = [...]` (M nhân w phải ra lại b).

Danh sách in ra theo dạng `[[a, b], [c, d]]` (dấu phẩy và một khoảng trắng, đúng như `print` của Python cho danh sách số nguyên).

Chạy: `python matran.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L02 matran.py`.
