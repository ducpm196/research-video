# Lab DVO L05 — Đối chiếu Hạ tầng dạng mã khai báo (lũy đẳng) vs mệnh lệnh

Đọc `stdin` `init=<int> target=<int> delta=<int>`. Chạy lặp 2 lần hàm khai báo đặt mức `target` so với hàm mệnh lệnh cộng dồn `delta` từ trạng thái `init`.

In đúng 3 dòng: `decl_after_2_runs=<d>`, `imp_after_2_runs=<d>`, `decl_is_idempotent=<0|1>`.
Chấm tự động: `bash labs/cham.sh DVO L05 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
