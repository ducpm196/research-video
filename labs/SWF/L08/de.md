# Lab SWF L08 — Máy trạng thái hữu hạn đèn giao thông có kiểm chứng chuyển tiếp

Đọc `stdin` `start=<STATE> seq=<S1,S2,...> bad_from=<STATE> bad_to=<STATE>`. Chạy chuỗi chuyển trạng thái theo bảng cho phép (`RED->GREEN->YELLOW->RED`) và kiểm tra nhảy tắt bị từ chối.

In đúng 3 dòng: `valid_cycle_ok=<0|1>`, `skip_green_to_red_rejected=<0|1>`, `final_state=<STATE>`.
Chấm tự động: `bash labs/cham.sh SWF L08 duong_dan/bai_cua_ban.py`
