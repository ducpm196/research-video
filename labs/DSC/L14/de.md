# Lab DSC L14 — Ước lượng điểm kèm khoảng tin cậy 95% (điểm phần trăm)

Đọc `stdin` `p1=<float> p2=<float> n=<int>`. Tính chênh lệch điểm phần trăm `(p2 - p1) * 100` và biên độ khoảng tin cậy 95% với hai nhóm cùng cỡ `n`.

In 1 dòng: `lift_pp=<.1f> ci95=[<.1f>, <.1f>]`.
Chấm tự động: `bash labs/cham.sh DSC L14 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
