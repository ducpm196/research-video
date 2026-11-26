# Lab MLO L06 — Gộp lô phục vụ: độ trễ chờ đợi và thông lượng

Đọc `stdin` `arr_rps=<f> batch=<int> single_ms=<f> batch_ms=<f>`. Tính thời gian chờ yêu cầu đầu `(batch-1)*(1000/arr_rps)`, thông lượng chạy đơn và chạy lô.

In 1 dòng: `first_wait_ms=<d> single_rps=<d> batch_rps=<d>`.
Chấm tự động: `bash labs/cham.sh MLO L06 duong_dan/bai_cua_ban.py`
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Làm tròn tất cả kết quả nguyên bằng định dạng `:.0f` của Python.
