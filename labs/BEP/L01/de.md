# Lab BEP L01 — TDD Red–Green–Refactor & Kiểm thử thành phần

Đọc từ `stdin` 2 dòng:
- Dòng 1: `balance=<int>`
- Dòng 2: `ops=<a1,a2,...>` (danh sách các số tiền cần chuyển liên tiếp)

Yêu cầu:
1. Mô phỏng giao dịch theo hợp đồng chuẩn: mỗi khoản rút `amt` hợp lệ khi `amt > 0` và `current_bal >= amt` (trả mã `200`, trừ `current_bal`); ngược lại giữ nguyên số dư và trả mã `422`.
2. So sánh với hàm stub hỏng luôn trả `200` không kiểm tra biên để đếm `red_caught` (số giao dịch hợp đồng đúng trả về khác hàm stub).
3. In đúng 3 dòng: `final_balance=<int>`, `rejected_count=<int>`, `red_caught=<int>`.

Chấm tự động: `bash labs/cham.sh BEP L01 duong_dan/bai_cua_ban.py`
