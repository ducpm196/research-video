# Lab DVO L06 — Quét rò rỉ bí mật và kiểm tra bí mật tồn tại trong lịch sử commit

Đọc `stdin` từng dòng (mỗi dòng là một bản ghi commit theo thứ tự thời gian, dòng cuối là `HEAD`). Quét biểu thức chính quy `sk_live_[0-9a-zA-Z]+` trên từng dòng để kiểm trạng thái `HEAD` cuối (`0|1`), đếm tổng số bản ghi rò rỉ và quyết định có cần xoay vòng khoá không (`1` nếu `history_leaked_commits > 0`).

In đúng 3 dòng: `head_has_secret=<0|1>`, `history_leaked_commits=<d>`, `rotation_required=<0|1>`.
Chấm tự động: `bash labs/cham.sh DVO L06 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
