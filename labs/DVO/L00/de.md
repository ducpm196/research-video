# Lab DVO L00 — Tìm kiếm nhị phân bằng lệnh git bisect

Đọc `stdin` `n1=<int> n2=<int> bad=<int>`. Tính số bước chia đôi tối đa cho hai quy mô lịch sử `n1`, `n2` (tức số nguyên `k` nhỏ nhất sao cho `2**k >= n`: có thể lặp nhân đôi `cur = 1; while cur < n: cur *= 2; k += 1` hoặc dùng `math.ceil(math.log2(n))`) và tìm nhị phân vị trí commit hỏng đầu tiên `bad` trong `[0, n2-1]`.

In đúng 3 dòng: `bisect_steps_3=<d>`, `bisect_steps_300=<d>`, `found_bad_commit=<d>`.
Chấm tự động: `bash labs/cham.sh DVO L00 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
