# Lab AIF L02 — Hàm đánh giá A*: h1 ô sai chỗ và Manhattan h2

Đọc `stdin` `board=<9 số 0..8> hstar=<int>`. Tính `h1` (số ô khác 0 sai vị trí), tổng khoảng cách Manhattan `h2`, và kiểm tính chấp nhận được `h1 <= h2 <= hstar`.

In 1 dòng: `h1=<d> h2=<d> admissible=<0|1>`.
Chấm tự động: `bash labs/cham.sh AIF L02 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
