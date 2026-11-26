# Lab SWF L09 — Kiểm tổ hợp xen kẽ trong bài toán tranh chấp hai luồng

Đọc `stdin` `ops_per_thread=<int>`. Với hai luồng mỗi luồng tăng `x += 1` qua `ops_per_thread` vòng (3 thao tác nguyên tử đọc–cộng–ghi mỗi vòng), đếm mọi kịch bản xen kẽ và kiểm có nhánh làm mất cập nhật hay không.

In đúng 3 dòng: `total_interleavings=<d>`, `distinct_x=<vals>`, `buggy_paths_gt0=<0|1>`.
Chấm tự động: `bash labs/cham.sh SWF L09 duong_dan/bai_cua_ban.py`
